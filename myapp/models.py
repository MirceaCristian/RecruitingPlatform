from django.contrib.auth.models import AbstractUser, User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from proiect_django import settings


class WorkField(models.Model):
    work_field = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.work_field


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    profession = models.ForeignKey(WorkField, on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)


class CV(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    field_of_work = models.ForeignKey(WorkField, on_delete=models.CASCADE, null=True, blank=True)
    cv_file = models.FileField(upload_to='static/CVs/')

    class Meta:
        app_label = 'myapp'

    def __str__(self):
        return f"{self.user} : {self.cv_file.name}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return (f"e-mail: {self.email}, name: {self.name}, subject: {self.subject}, message: {self.message},"
                f" phone: {self.phone}")


@receiver(post_save, sender=Contact)
def send_mail(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='New contact on the platform',
            message=f'new contact: {instance}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER]
        )


class Job(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    field_of_work = models.ForeignKey(WorkField, on_delete=models.CASCADE, blank=True, null=True)
