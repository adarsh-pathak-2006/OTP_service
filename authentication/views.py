from django.shortcuts import render
from .serializer import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q

class RegisterAPI(APIView):
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            password=serial.validated_data['password']
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'message':'username or email already exists'}, status=400)
            User.objects.create_user(username=username, email=email, password=password)
            return Response({'message':'Registration Successfull'}, status=201)
        return Response(serial.errors, status=400)