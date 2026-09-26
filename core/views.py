from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializer import ProjectSerializer, OTPSerializer
from .models import Project, OTP

class DashboardAPI(ListAPIView):
    serializer_class=ProjectSerializer

    def get_queryset(self):
        return Project.objects.select_related('user').filter(user=self.request.user)

class ProjectDetailAPI(RetrieveAPIView):
    serializer_class=ProjectSerializer

    def get_queryset(self):
        return Project.objects.select_related('user').filter(user=self.request.user)