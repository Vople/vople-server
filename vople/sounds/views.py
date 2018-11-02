from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializsers

# Create your views here.
class ListAllBoards(APIView):
    def get(self, request, format=None):

        all_boards = models.Board.objects.all()

        serializer = serializsers.BoardSerializer(all_boards, many=True)

        return Response(data=serializer.data)


class ListAllComments(APIView):
    def get(self, request, format=None):

        all_comments = models.Comment.objects.all()

        serializer = serializsers.CommentSerializer(all_comments, many=True)

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