from django.contrib.auth.models import AbstractUser, User
from django.db import models


# class CustomUser(AbstractUser):
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=11, unique=True)


class CV(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    cv_file = models.FileField(upload_to='')

    class Meta:
        app_label = 'myapp'

    def __str__(self):
        return f"{self.name} {self.surname}"
