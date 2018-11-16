from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from . import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'username',
            'name',
            'gender',
            'followers',
            'following',
        )

class CustomRegistrationSerializer(RegisterSerializer):

    name = serializers.CharField(required=True)
    bio = serializers.CharField(required=False)
    gender = serializers.CharField(required=True)

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name','')
        user.bio = self.validated_data.get('bio','')
        user.gender = self.validated_data.get('gender', '')
        user.save(update_fields=['name', 'bio', 'gender'])

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'name',
        )