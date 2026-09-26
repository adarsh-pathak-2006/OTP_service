from rest_framework.serializers import ModelSerializer
from .models import Project, OTP
from authentication.serializer import UserGetSerializer

class PRojectSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Project
        fields='__all__'
        read_only_fields=['refrence_id', 'created_on']

class OTPSerializer(ModelSerializer):
    project=PRojectSerializer(read_only=True)
    class Meta:
        model=OTP
        fields='__all__'
        read_only_fields=['otp', 'sent_on']