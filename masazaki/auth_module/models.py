from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# ? Are jsonfields good for indexing
# ? Services should be added in a separate table
# ? Add an instantly available field
# add signals for profile creation

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    # Should hold either of these three therapist, regular_client or spa
    client_type =   models.CharField(max_length=254, null=True)
    
    about =   models.CharField(max_length=1000, null=True)
    # Should hold either Male, Female or None
    gender =   models.CharField(max_length=6, null=True)
    # Should hold url to our hosted image 
    profile_picture_url = models.URLField(max_length = 200, null=True)
    # Should be an aggregate of address, city, country
    address = models.CharField(max_length=254, null=True)
    city = models.CharField(max_length=254, null=True)
    country = models.CharField(max_length=254, null=True)
    is_email_verified = models.BooleanField(default=False, null=True)
    phone_number = models.CharField(max_length=254, null=True)
    is_sms_verified = models.BooleanField(default=False, null=True)
    # Should be either strict;1, medium:0 or felxible:-1
    cancelation_policy = models.CharField(max_length=1, null=True)
    # Should hold only numeric value
    rate_per_hour = models.CharField(max_length=254, null=True)
    allows_bed_massage = models.BooleanField(default=False, null=True)
    allows_spa = models.BooleanField(default=False, null=True)
    is_taxpayer = models.BooleanField(default=False, null=True)
    services_and_costs = models.JSONField(null=True)
    qualification = models.JSONField(null=True)
    experience = models.JSONField(null=True)
    availability = models.JSONField(null=True)
    areas_of_availability = ArrayField(models.CharField(max_length=200), null=True)
    # For spas only
    number_of_employees = models.PositiveIntegerField(default=0, null=True)
    # For db record
    
    modified_at =   models.DateTimeField(default=timezone.now)
    is_featured =   models.BooleanField(default=False, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


# User._meta.get_field('email')._unique = True

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Should hold either of these three therapist, regular_client or spa
#     client_type =   models.CharField(max_length=254, null=True)
#     # Would hold name of spa in case client's a spa
#     first_name =   models.CharField(max_length=254, null=True)
#     last_name =   models.CharField(max_length=254, null=True)
#     about =   models.CharField(max_length=1000, null=True)
#     # Should hold either Male, Female or None
#     gender =   models.CharField(max_length=6, null=True)
#     # Should hold url to our hosted image 
#     profile_picture_url = models.URLField(max_length = 200, null=True)
#     # Should be an aggregate of address, city, country
#     address = models.CharField(max_length=254, null=True)
#     city = models.CharField(max_length=254, null=True)
#     country = models.CharField(max_length=254, null=True)
#     email_address = models.EmailField(max_length=254, null=True)
#     is_email_verified = models.BooleanField(default=False, null=True)
#     phone_number = models.CharField(max_length=254, null=True)
#     is_sms_verified = models.BooleanField(default=False, null=True)
#     # Should be either strict;1, medium:0 or felxible:-1
#     cancelation_policy = models.CharField(max_length=1, null=True)
#     # Should hold only numeric value
#     rate_per_hour = models.CharField(max_length=254, null=True)
#     allows_bed_massage = models.BooleanField(default=False, null=True)
#     allows_spa = models.BooleanField(default=False, null=True)
#     is_taxpayer = models.BooleanField(default=False, null=True)
#     services_and_costs = models.JSONField(null=True)
#     qualification = models.JSONField(null=True)
#     experience = models.JSONField(null=True)
#     availability = models.JSONField(null=True)
#     # areas_of_availability = ArrayField(models.CharField(max_length=200), null=True)
#     # For spas only
#     number_of_employees = models.PositiveIntegerField(default=0, null=True)
#     # For db record
#     created_at  =   models.DateTimeField(default=datetime.now(timezone.utc))
#     modified_at =   models.DateTimeField(default=datetime.now(timezone.utc))
#     is_featured =   models.BooleanField(default=False, null=True)


# @receiver(post_save, sender=User)
# def embellish_registration(sender, instance=None, created=False, **kwargs):
#     if created:
#         # Token.objects.create(user=instance)
#         # print('Token created...')
#         Profile.objects.create(user=instance)
#         print('Profile created...')