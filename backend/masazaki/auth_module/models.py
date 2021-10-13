from django.db import models
from django.contrib.auth.models import User

# add signals for profile creation
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
