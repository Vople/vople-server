from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vople.users import serializers as user_serializer
from vople.users import models as user_model
from . import models, serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

BOARD_FREE_MODE = 0
BOARD_ROLE_MODE = 1

# Create your views here.
class ListAllBoards(APIView):

    def get(self, request, format=None):

        boards = models.Board.objects.all()

        paginator = Paginator(boards, 20)

        page = request.GET.get('page')

        try:
            boards = paginator.page(page)
        except PageNotAnInteger:
        
            boards = paginator.page(1)
        except EmptyPage:
            boards = paginator.page(paginator.num_pages)


        serializer = serializers.BoardBreifSerializer(boards, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):

        user = request.user

        serializer = serializers.InputBoardSerializer(data=request.data)

        present_id = request.data['present_id']

        mode = request.data['mode']

        script_id = request.data['script_id']

        try:
            found_present = models.Present.objects.get(id=present_id)
        except models.Present.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            found_script = models.Script.objects.get(id=script_id)
        except models.Script.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save(
                owner = user,
                present = found_present,
                mode=mode,
                script=found_script,
                )

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinBoardViewSet(APIView):

    def get(self, request, board_id, format=None):

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if found_board.mode == BOARD_FREE_MODE:
            return Response(status=status.HTTP_200_OK)

        member_restriction = found_board.script.member_restriction

        current_members = found_board.joined_member.all().count()

        if member_restriction <= current_members:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        edible_rolls = []

        for cast in found_board.script.casts.all():
            if cast.is_adjust == False:
                if cast.roll_name not in edible_rolls:
                    edible_rolls.append(cast.roll_name)

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
            return Response(status=status.HTTP_200_OK)

        try:
            found_cast = found_board.script.casts.get(roll_name=roll_name)
        except models.Cast.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        found_plots = found_cast.plots.all()

        if len(found_plots) <= 0 :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        found_cast.is_adjust = True

        found_cast.member = user
        
        found_cast.save()

        return Response(status=status.HTTP_200_OK)


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
        pass
        # user = request.user

        # try:
        #     found_board = models.Board.objects.get(id=board_id)
        # except models.Board.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        # serializer = serializers.InputSoundSerializer(data=request.data)

        # if found_board.mode = BOARD_FREE_MODE:
        #     if serializer.is_valid():
        #         serializer.save(
        #             owner = user,
        #             board = found_board
        #         )
        #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # else :
        #     plot_id = request.data['plot_id']


        
        
        #     found_plot = models.Plot.objects.get(id=plot_id)
        # return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            

class BoardDetailView(APIView):

    def get(self, request, board_id, format=None):

        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.BoardSerializer(found_board)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ScriptViewSet(APIView):

    def get(self, request, format=None):
        
        scripts = models.Script.objects.filter()

        serializer = serializers.ScriptSerializer(scripts, many=True)

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