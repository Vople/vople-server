from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vople.users import serializers as user_serializer
from vople.users import models as user_model
from . import models, serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from fcm.utils import get_device_model
from rest_framework import viewsets

BOARD_FREE_MODE = 0
BOARD_ROLE_MODE = 1

def CheckBoardTerminated(board):
    
    if board.mode == BOARD_FREE_MODE:
        return False

    script = board.script

    plots = script.plots_by_cast.all()

    null_count = plot.filter(comment__isnull=True).count()

    if null_count > 0:
        return False
    else:
        return True

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = models.MyDevice.objects.all()
    serializer_class = serializers.DeviceSerializer

    def post(self, request, format=None):

        device = models.MyDevice.objects.filter(dev_id=request.data['dev_id'])

        if device.count() == 0 :
            serializer = serializers.DeviceSerializer(data=request.data)
        else :
            device = device.first()
            serializer = serializers.DeviceSerializer(device, data=request.data)

        if serializer.is_valid():

            serializer.save(name=request.user.username, user_id=request.user.id,is_active=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        device = models.MyDevice.objects.filter(name=request.user.username)

        if device.count() == 0:
            return Response(status=401)

        device=device.first()

        if request.data['is_active'] == 'true':
            device.is_active = True
        else :
            device.is_active = False

        device.save()

        return Response(status=200)

# Create your views here.
class ListAllBoards(APIView):

    def get(self, request, format=None):

        boards = models.Board.objects.all()

        paginator = Paginator(boards, 100)

        page = request.GET.get('page')

        try:
            boards = paginator.page(page)
        except PageNotAnInteger:
        
            boards = paginator.page(1)
        except EmptyPage:
            boards = paginator.page(paginator.num_pages)

        serializer = serializers.BoardBreifSerializer(boards, many=True)

        # Device = get_device_model()

        # try:
        #     devices = Device.objects.filter(user=request.user)
        # except Device.DoesNotExist:
        #     return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        # if not devices.count()==0 :
        #     testDevice=cafeDevice.first()
        # else:
        #     testDevice = devices
                    
        # testDevice.send_message(data={"test": "test"})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):

        user = request.user

        serializer = serializers.InputBoardSerializer(data=request.data)

        mode = request.data['mode']

        if(mode == BOARD_FREE_MODE):
            if serializer.is_valid():
                new_board = serializer.save(
                    owner=user,
                    mode=BOARD_FREE_MODE, 
                    script=None)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else: 
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        script_id = request.data['script_id']

        try:
            found_script = models.Script.objects.get(id=script_id)
        except models.Script.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            board = serializer.save(
                owner=user,
                mode=mode,
                script=found_script,
                )

            found_casts = models.Cast.objects.filter(script_title=found_script.title)

            for cast in found_casts:
                new_casting = models.Casting.objects.create(
                    board=board,
                    script=found_script,
                    cast=cast,
                )

                new_casting.save()

            serializer = serializers.BoardBreifSerializer(board)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinBoardViewSet(APIView):

    def get(self, request, board_id, format=None):

        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if found_board.mode == BOARD_FREE_MODE:
            return Response(status=status.HTTP_200_PARTIAL_CONTENT)

        flag_join_accept = True

        try:
            _user = found_board.joined_member.all().get(id=user.id)
        except user_model.User.DoesNotExist:
            flag_join_accept = False

        # Already Joined
        if(flag_join_accept):
            
            serializer = serializers.EdibleRollNumberSerializer(data={"rolls":[]})

            if serializer.is_valid():
                return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        member_restriction = found_board.script.member_restriction

        current_members = found_board.joined_member.all().count()

        if member_restriction <= current_members:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        edible_rolls = []

        for casting in found_board.castings.all():
            if casting.is_adjust == False:
                if casting.cast.roll_name not in edible_rolls:
                    edible_rolls.append(casting.cast.roll_name)

        if len(edible_rolls) <= 0 :
            return Response(status=status.HTTP_204_NO_CONTENT)

        rolls = {"rolls" : edible_rolls}

        serializer = serializers.EdibleRollNumberSerializer(data=rolls)

        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, board_id, format=None):
        
        user = request.user

        roll_name = request.data['roll_name']

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if found_board.mode == BOARD_FREE_MODE:
            found_board.joined_member.add(user)
            found_board.save()
            return Response(status=status.HTTP_200_OK)

        found_casting = None
        
        for casting in found_board.castings.all():
            if casting.cast.roll_name == roll_name:
                found_casting = casting
                    
        if found_casting == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if found_casting.is_adjust == True:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        found_plots = found_casting.cast.plots_by_cast.all()

        if len(found_plots) <= 0 :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        found_casting.is_adjust = True

        found_casting.member = user
        
        found_casting.save()

        found_board.joined_member.add(user)

        found_board.save()

        serializer = serializers.CastingSerializer(found_casting)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, board_id, format=None):
        
        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if found_board.mode == BOARD_FREE_MODE:
            return Response(status=status.HTTP_200_OK)

        try:
            found_casting = found_board.castings.get(member=user)
        except models.Casting.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CastingSerializer(found_casting)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


class ListAllComments(APIView):

    def get(self, request, format=None):

        all_comments = models.Comment.objects.all()

        serializer = serializers.CommentSerializer(all_comments, many=True)

        return Response(data=serializer.data)

class ListCommentsOnBoard(APIView):

    def get(self, request, board_id, format=None):

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        all_comments = found_board.comments

        serializer = serializers.CommentSerializer(all_comments, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListAllBoardLikes(APIView):

    def get(self, request, format=None):

        all_board_likes = models.BoardLike.objects.all()

        serializer = serializers.BoardLikeSerializer(all_board_likes, many=True)

        return Response(data=serializer.data)

class ListAllCommentLikes(APIView):

    def get(self, request, format=None):

        all_comment_likes = models.CommentLike.objects.all()

        serializer = serializers.CommentLikeSerializer(all_comment_likes, many=True)

        return Response(data=serializer.data)

class ListAllPresents(APIView):
    
    def get(self, request, format=None):

        all_presents = models.Present.objects.all()

        serializer = serializers.PresentSerializer(all_presents, many=True)

        return Response(data=serializer.data)

class LikeBoard(APIView):
    def post(self, request, board_id, format=None):

        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preExtistingLike = models.BoardLike.objects.get(
                owner=user,
                board=found_board
            )
            preExtistingLike.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.BoardLike.DoesNotExist:

            new_like = models.BoardLike.objects.create(
                owner=user,
                board=found_board
            )

            new_like.save()

            return Response(status=status.HTTP_201_CREATED)

class LikeComment(APIView):

    def get(self, request, comment_id, format=None):
        likes = models.CommentLike.objects.filter(comment__id = comment_id)

        likes_id = likes.values('owner_id')

        users = user_model.User.objects.filter(id__in=likes_id)

        serializer = user_serializer.ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, comment_id, format=None):

        user = request.user

        try:
            found_comment = models.Comment.objects.get(id=comment_id)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preExtistingLike = models.CommentLike.objects.get(
                owner=user,
                comment=found_comment
            )
            preExtistingLike.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.CommentLike.DoesNotExist:

            new_like = models.CommentLike.objects.create(
                owner=user,
                comment=found_comment
            )

            new_like.save()

            return Response(status=status.HTTP_201_CREATED)

class CommentOnBoard(APIView):

    def post(self, request, board_id, format=None):

        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.InputSoundSerializer(data=request.data)

        if found_board.mode == BOARD_FREE_MODE:
            if serializer.is_valid():
                serializer.save(
                    owner = user,
                    board = found_board
                )
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else :
            plot_id = int(request.data['plot_id'])

            try:
                found_plot = models.Plot.objects.get(id=plot_id)
            except models.Plot.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if serializer.is_valid():
                new_comment = serializer.save(
                    owner = user,
                    board = found_board
                )
            else:
                return Response(data=serializer.errors, status=status.HTTP_402_PAYMENT_REQUIRED)

            new_commenting = models.Commenting.objects.create(
                board=found_board,
                comment=new_comment
            )

            new_commenting.save()

            found_plot.commenting = new_commenting

            found_plot.save()

            # if(CheckBoardTerminated(found_board)):
            #     # FCM to Manager
            # else:
                    
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            

class BoardDetailView(APIView):

    def get(self, request, board_id, format=None):

        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.BoardDetailSerializer(found_board)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ScriptViewSet(APIView):

    def get(self, request, format=None):
        
        scripts = models.Script.objects.all()

        serializer = serializers.ScriptNameSerializer(scripts, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)        

    def post(self, request, format=None):
        
        user = request.user

        member_restriction = request.data.get('member_restriction', -1)

        title = request.data.get('title', '')

        plots = request.data.get('plots')

        if(member_restriction <= 0 or len(plots) <= 0 or member_restriction != len(plots)):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        new_script = models.Script.objects.create(
            owner=user,
            member_restriction=member_restriction,
            title=title,
        )

        new_script.save()

        for i in range(0, member_restriction):
            plot = models.Plot.objects.create(
                content=plots.get('plots' + str(i)),
                script=new_script,
            )
            plot.save()

        return Response(status=status.HTTP_201_CREATED)

class GetScriptView(APIView):
    def get(self, request, script_id, format=None):

        try:
            found_script = models.Script.objects.get(id=script_id)
        except models.Script.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ScriptSerializer(found_script)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class GetPlotView(APIView):
    def get(self, request, board_id, format=None):
        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        script = found_board.script

        castings = found_board.castings.all()

        found_casting = None

        for casting in castings:
            if casting.member == user:
                found_casting = casting

        if found_casting == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        plots = found_casting.cast.plots_by_cast.all()

        serializer = serializers.PlotSerializer(plots, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetEventBoardView(APIView):
    def get(self, request, format=None):

        event_boards = models.Board.objects.filter(owner__id=1)

        serializer = serializers.BoardBreifSerializer(event_boards, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
