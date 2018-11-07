from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView

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

    name = serializers.CharField(max_lenth="20", required=True)
    bio = serializers.TextField(required=False)
    gender = CharField(max_length=80, null=True)

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name','')
        user.bio = self.validated_data.get('bio','')
        user.gender = self.validated_data.get('gender', '')
        user.save(update_fields=['name', 'bio', 'gender'])


class CustomRegistrationView(RegisterView):
    serializer_class = CustomRegistrationSerializer