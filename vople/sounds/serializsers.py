from rest_framework import serializers
from . import models

class BoardSerializer(serializers.Serializer):

    class Meta:
        model = models.Board
        fields = '__all__'

class CommentSerializer(serializers.Serializer):

    class Meta:
        model = models.Comment
        fields = '__all__'

class BoardLikeSerializer(serializers.Serializer):

    class Meta:
        model = mdoels.BoardLike
        fields = '__all__'

class CommentLikeSerializer(serializers.Serializer):

    class Meta:
        model = models.CommentLike
        fields = '__all__'