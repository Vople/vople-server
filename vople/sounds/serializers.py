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

class PresentSerializer(serializers.ModelSerializer):
    
    owner = UserSerializer()

    class Meta:
        model = models.Present
        fields = '__all__'



class CastBreifSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cast
        fields = (
            'roll_name',
            'script_title',
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


class CommentingSerializer(serializers.ModelSerializer):

    comment = CommentBriefSerializer()
    board = BoardBreifSerializer()

    class Meta:
        model = models.Commenting
        fields = (
            'board',
            'comment',
        )


class PlotSerializer(serializers.ModelSerializer):

    commenting = CommentingSerializer()

    class Meta:
        model = models.Plot
        fields = (
            'id',
            #'content',
            'commenting',
            'order',
        )

class CastSerializer(serializers.ModelSerializer):

    plots_by_cast = PlotSerializer()

    class Meta:
        model = models.Cast
        fields = (
            'id',
            'roll_name',
            'script_title',
            'plots_by_cast',
        )


class ScriptSerializer(serializers.ModelSerializer):

    casts = CastSerializer(many=True)

    class Meta:
        model = models.Script
        fields = (
            'id',
            'member_restriction',
            'casts',
            'title',
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

class CastingSerializer(serializers.ModelSerializer):

    cast = CastSerializer()

    class Meta:
        model = models.Casting
        fields = (
            'id',
            'cast',
            'member',
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
