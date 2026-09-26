from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Project, OTP
from otp.cache_keys import projectList_key, OTPList_key
from django.core.cache import cache

@receiver(post_save, sender=Project)
def projectlistcacheinvalidation(sender, instance, created, **kwargs):
    for i in range(1, 100):
        cache.delete(projectList_key(pageno=i, userid=instance.user.id))

@receiver(post_save, sender=OTP)
def otplistcacheinvalidation(sender, instance, created, **kwargs):
    for i in range(1, 100):
        cache.delete(OTPList_key(pageno=i, projid=instance.project.id))