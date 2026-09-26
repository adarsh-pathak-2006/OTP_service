from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Project, OTP
from otp.cache_keys import projectList_key, OTPList_key
from django.core.cache import cache

@receiver(post_save, sender=Project)
def projectlistcacheinvalidation(sender, instance, created, **kwargs):
    cache.delete_pattern(f"projectsList_userid:{instance.user.id}_pageno:*")

@receiver(post_save, sender=OTP)
def otplistcacheinvalidation(sender, instance, created, **kwargs):
    cache.delete_pattern(f"OTPList_projectid:{instance.project.id}_pageno:*")