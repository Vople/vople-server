from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


        serializer = serializers.BoardSerializer(boards, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

        #queryset = models.Board.objects.all()
        #serializer_class = serializers.BoardSerializer

        #filter_backends = (filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
        #search_fields = ('job_name', 'company')
        #filter_fields = ('job_name', 'company')
        #ordering_fields = ('job_name','company')
        #ordering = ('job_name')

        #pagination_class = serializers.PaginatedBoardSerializer


        #return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        user = request.user

        serializer = serializers.InputBoardSerializer(data=request.data)

        gift_id = request.data['gift_id']

        try:
            found_gift = models.Gift.objects.get(id=gift_id)
        except models.Gift.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save(
                owner = user,
                gift = found_gift,
                )

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListAllComments(APIView):
    def get(self, request, format=None):

        all_comments = models.Comment.objects.all()

        serializer = serializers.CommentSerializer(all_comments, many=True)

        return Response(data=serializer.data)

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

class ListAllGifts(APIView):
    def get(self, request, format=None):

        all_gifts = models.Gift.objects.all()

        serializer = serializers.GiftSerializer(all_gifts, many=True)

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

        if serializer.is_valid():
            serializer.save(
                owner = user,
                board = found_board
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardDetailView(APIView):
    def get(self, request, board_id, format=None):

        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.BoardSerializer(found_board)

        return Response(data=serializer.data, status=status.HTTP_200_OK)