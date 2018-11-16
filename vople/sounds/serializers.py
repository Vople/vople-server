from rest_framework import serializers
from . import models
from vople.users.serializers import UserSerializer, UserBriefSerializer
from vople.users import models as user_model
from rest_framework import pagination

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MyDevice
        fields = (
            'dev_id',
            'reg_id',
            'name',
            'is_active'
            )

class ScriptBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Script
        fields = (
            'title',
        )


class CommentBriefSerializer(serializers.ModelSerializer):

    owner = UserBriefSerializer()

    class Meta:
        model = models.Comment
        fields = (
            'owner',
            'sound',
            'created_at',
        )


class ScriptNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Script
        fields = (
            'id',
            'title',
            'member_restriction',
        )

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

    comment = CommentBriefSerializer()

    class Meta:
        model = models.Plot
        fields = (
            'id',
            'content',
            'order',
            'comment',
        )

class CastSerializer(serializers.ModelSerializer):

    plots_by_cast = PlotSerializer(many=True)

    class Meta:
        model = models.Cast
        fields = (
            'id',
            'roll_name',
            'plots_by_cast',
            'member',

        )

class CastBreifSerializer(serializers.ModelSerializer):

    plots_by_cast = PlotSerializer(many=True)

    class Meta:
        model = models.Cast
        fields = (
            'roll_name',
            'plots_by_cast',
        )

class ScriptSerializer(serializers.ModelSerializer):

    casts = CastBreifSerializer(many=True)

    class Meta:
        model = models.Script
        fields = (
            'id',
            'member_restriction',
            'casts',
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

class BoardDetailSerializer(serializers.ModelSerializer):

    comments = CommentBriefSerializer(many=True)
    script = ScriptSerializer()

    class Meta:
        model = models.Board
        fields = (
            'title',
            'comments',
            'script',
        )

class BoardBreifSerializer(serializers.ModelSerializer):

    script = ScriptBriefSerializer()

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
        )

class EdibleRollNumberSerializer(serializers.Serializer):

    rolls = serializers.ListField(child=serializers.CharField(max_length=20))
