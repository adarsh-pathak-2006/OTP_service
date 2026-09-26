from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from otp.cache_keys import projectList_key, OTPList_key
from otp.pagination import GeneralPagination
from .serializer import ProjectSerializer, OTPSerializer
from .models import Project, OTP

class DashboardAPI(APIView):
    def get(self, request):
        page_no=request.query_params.get("page_no")
        key=projectList_key(pageno=page_no, userid=request.user.id)
        cached_data=cache.get(key=key)
        if cached_data:
            return Response(cached_data, status=200)
        paginator=GeneralPagination()
        data=paginator.paginate_queryset(Project.objects.select_related('user').filter(user=request.user).order_by("-created_on"))
        serial=ProjectSerializer(data, many=True)
        response=paginator.get_paginated_response(serial.data)
        cache.set(key, response.data, timeout=500)
        return response

class OTPListAPI(APIView):
    def get(self, request, pk):
        pageno=request.query_params.get("page_no")
        key=OTPList_key(pageno=pageno, projid=pk)
        cached_data=cache.get(key=key)
        if cached_data:
            return Response(cached_data, status=200)
        paginator=GeneralPagination()
        data=paginator.paginate_queryset(OTP.objects.select_related('project').filter(project__id=pk))
        serial=OTPSerializer(data, many=True)
        response=paginator.get_paginated_response(serial.data)
        cache.set(key, response.data, timeout=500)
        return response

