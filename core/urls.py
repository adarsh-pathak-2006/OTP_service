from django.urls import path
from .views import DashboardAPI, OTPListAPI

urlpatterns = [
    path('projects/', DashboardAPI.as_view()),
    path('projects/<int:pk>/', OTPListAPI.as_view())
]
