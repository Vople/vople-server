from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class ListAllBoards(APIView):
    def get(self, request, format=None):

        all_boards = models.Board.objects.all()

        paginator = Paginator(all_boards, 20)

        page = request.GET.get('page')

        try:
            boards = paginator.page(page)
        except PageNotAnInteger:
        
            boards = paginator.page(1)
        except EmptyPage:
            boards = paginator.page(paginator.num_pages)

        serializer = serializers.PaginatedBoardSerializer(all_boards, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        user = request.user

        serializer = serializers.InputBoardSerializer(data=request.data)

        present_id = request.data['present_id']

        try:
            found_present = models.Present.objects.get(id=present_id)
        except models.Present.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save(
                owner = user,
                present = found_present,
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
