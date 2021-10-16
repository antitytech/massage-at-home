from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# ? Are jsonfields good for indexing
# ? Services should be added in a separate table
# ? Add an instantly available field
# add signals for profile creation
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Should hold either of these three therapist, regular_client or spa
    client_type =   models.CharField(max_length=254)
    # Would hold name of spa in case client's a spa
    first_name =   models.CharField(max_length=254)
    last_name =   models.CharField(max_length=254)
    about =   models.CharField(max_length=1000)
    # Should hold either Male, Female or None
    gender =   models.CharField(max_length=6)
    # Should hold url to our hosted image 
    profile_picture_url = models.URLField(max_length = 200)
    # Should be an aggregate of address, city, country
    address = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    country = models.CharField(max_length=254)
    email_address = models.EmailField(max_length=254)
    is_email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=254)
    is_sms_verified = models.BooleanField(default=False)
    # Should be either strict;1, medium:0 or felxible:-1
    cancelation_policy = models.CharField(max_length=1)
    # Should hold only numeric value
    rate_per_hour = models.CharField(max_length=254)
    allows_bed_massage = models.BooleanField(default=False)
    allows_spa = models.BooleanField(default=False)
    is_taxpayer = models.BooleanField(default=False)
    services_and_costs = models.JSONField()
    qualification = models.JSONField()
    experience = models.JSONField()
    availability = models.JSONField()
    areas_of_availability = ArrayField(models.CharField(max_length=200), blank=True)
    # For spas only
    number_of_employees = models.PositiveIntegerField(default=0)
    # For db record
    created_at  =   models.DateTimeField()
    modified_at =   models.DateTimeField()
    is_featured =   models.BooleanField(default=False)
