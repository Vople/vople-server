from rest_framework import serializers
from . import models
from vople.users.serializers import UserSerializer
from rest_framework import pagination


class GiftSerializer(serializers.ModelSerializer):
    
    owner = UserSerializer()

    class Meta:
        model = models.Gift
        fields = '__all__'



class CommentLikeSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)

    class Meta:
        model = models.CommentLike
        fields = '__all__'


class EventLikeSerializer(serializers.ModelSerializer):
    
    owner = UserSerializer()

    class Meta:
        model = models.EventLike
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


class EventSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    present = GiftSerializer()
    comments = CommentSerializer(many=True)
    event_likes = EventLikeSerializer(many=True)

    class Meta:
        model = models.Event
        fields = (
            'id',
            'owner',
            'present',
            'title',
            'content',
            'due_date',
            'comments',
            'event_likes',
        )

class InputSoundSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = (
            'sound',
        )
        
class InputEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = (
            'title',
            'content',
            'due_date',
        )
