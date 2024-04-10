from django.contrib.auth.models import AbstractUser, User
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)


class CV(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cv_file = models.FileField(upload_to='static/CVs/')

    class Meta:
        app_label = 'myapp'

    def __str__(self):
        return f"{self.user}"
