from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class UserGetSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email']

class RegisterSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'password']