from rest_framework import serializers
from . import models
from vople.users.serializers import UserSerializer
from vople.users import models as user_model
from rest_framework import pagination

class UserBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model.User
        fields = (
            'name',
        )

class PresentSerializer(serializers.ModelSerializer):
    
    owner = UserSerializer()

    class Meta:
        model = models.Present
        fields = '__all__'


class PlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Plot
        fields = (
            'id',
            'content',
        )

class ScriptSerializer(serializers.ModelSerializer):

    plots = PlotSerializer(many=True)

    class Meta:
        model = models.Script
        fields = (
            'id',
            'owner',
            'member_restriction',
            'plots',
            'title',
        )




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
    owner = UserBriefSerializer()

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

    owner = UserBriefSerializer()
    comments = CommentSerializer(many=True)
    board_likes = BoardLikeSerializer(many=True)
    script = ScriptSerializer()
    
    class Meta:
        model = models.Board
        fields = (
            'id',
            'owner',
            'title',
            'content',
            'due_date',
            'comments',
            'board_likes',
            'script',
            'joined_member',
        )

class BoardBreifSerializer(serializers.ModelSerializer):

    script = ScriptSerializer()

    class Meta:
        model = models.Board
        fields = (
            'id',
            'title',
            'mode',
            'script',
            'board_likes',
        )

class InputSoundSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = (
            'sound',
        )
        
class InputBoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Board
        fields = (
            'title',
            'content',
            'due_date',
        )

class EdibleRollNumberSerializer(serializers.Serializer):

    rolls = serializers.ListField(child=serializers.CharField(max_length=20))
