from rest_framework import serializers
from . import models
from vople.users.serializers import UserSerializer


class PresentSerializer(serializers.ModelSerializer):
    
    owner = UserSerializer()

    class Meta:
        model = models.Present
        fields = '__all__'



class CommentLikeSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)

    class Meta:
        model = models.CommentLike
        fields = '__all__'


class BoardLikeSerializer(serializers.ModelSerializer):
    
    owner = UserSerializer()

    class Meta:
        model = models.BoardLike
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):

    comment_likes = CommentLikeSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'owner',
            'content',
            'sound',
            'comment_likes',
        )


class BoardSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    present = PresentSerializer()
    comments = CommentSerializer(many=True)
    board_likes = BoardLikeSerializer(many=True)

    class Meta:
        model = models.Board
        fields = (
            'id',
            'owner',
            'present',
            'title',
            'content',
            'due_date',
            'comments',
            'board_likes',
        )

class InputSoundSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = (
            'sound',
        )
        