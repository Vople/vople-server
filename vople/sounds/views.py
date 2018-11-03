from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers

# Create your views here.
class ListAllBoards(APIView):
    def get(self, request, format=None):

        all_boards = models.Board.objects.all()

        serializer = serializers.BoardSerializer(all_boards, many=True)

        return Response(data=serializer.data)


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
    def get(self, request, board_id, format=None):

        user = request.user

        try:
            found_board = models.Board.objects.get(id=board_id)
        except models.Board.DoesNotExist:
            return Response(status=404)

        try:
            preExtistingLike = models.BoardLike.objects.get(
                owner=user,
                board=found_board
            )
            preExtistingLike.delete()
        except models.BoardLike.DoesNotExist:

            new_like = models.BoardLike.objects.create(
                owner=user,
                board=found_board
            )

            new_like.save()

            return Response(status=200)


class LikeComment(APIView):
    def get(self, request, comment_id, format=None):

        user = request.user

        try:
            found_comment = models.Comment.objects.get(id=comment_id)
        except models.Comment.DoesNotExist:
            return Response(status=404)

        try:
            preExtistingLike = models.CommentLike.objects.get(
                owner=user,
                comment=found_comment
            )
            preExtistingLike.delete()
        except models.Comment.DoesNotExist:

            new_like = models.CommentLike.objects.create(
                owner=user,
                comment=found_comment
            )

            new_like.save()

            return Response(status=200)