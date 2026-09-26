from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    reference_id=models.CharField(max_length=10)
    project_name=models.CharField(max_length=50, default='New Project')
    description=models.TextField(null=True)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

class OTP(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    email=models.EmailField()
    otp=models.CharField(max_length=6)
    sent_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project.project_name
    
