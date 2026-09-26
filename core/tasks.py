from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def sendOTPToEmail(email, otp):
    send_mail(
        subject="OTP for registration",
        message=f"The OTP for registering in the website otp:{otp}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return f"OTP sent to {email} OTP:{otp}"