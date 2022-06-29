from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
