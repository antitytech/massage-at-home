from django.db import models
from django.contrib.auth.models import User
from auth_module.models import Profile

# Create your models here.
class JobPost(models.Model):
    # These are job posts by spa client
    author      =       models.OneToOneField(User, on_delete=models.CASCADE, related_name='post_author')
    title       =       models.CharField(max_length=254)
    services    =       models.JSONField()
    descrption  =       models.CharField(max_length=1000)
    is_featured =       models.BooleanField(default=False)
    duration    =       models.DurationField()
    created_at  =       models.DateTimeField()
    modified_at =       models.DateTimeField()
    rate        =       models.PositiveIntegerField()

class Offer(models.Model):
    # ? Can add more fields to it
    # Sender could be client or spa
    sender          =   models.OneToOneField(User, on_delete=models.CASCADE, related_name='offer_sender')
    therapist       =   models.OneToOneField(User, on_delete=models.CASCADE, related_name='offer_receiver')
    # Should hold requested or accepted
    status          =   models.CharField(max_length=254)

class Appointment(models.Model):
    # ? Can add more fields to it
    hiree           =       models.OneToOneField(User, on_delete=models.CASCADE, related_name='hiree')
    hirer           =       models.OneToOneField(User, on_delete=models.CASCADE, related_name='hirer')
    offer           =       models.OneToOneField(Offer, on_delete=models.CASCADE, related_name='offer')
    created_at      =       models.DateTimeField()
    due_on          =       models.DateTimeField()
    # It will hold due, missed, cancelled, done
    status          =       models.CharField(max_length=100)
    is_approved     =       models.BooleanField(default=False)

class Payment(models.Model):
    # ? Can add more fields to it
    payer       =       models.OneToOneField(User, on_delete=models.CASCADE, related_name='payer')
    payee       =       models.OneToOneField(User, on_delete=models.CASCADE, related_name='payee')
    appointment       =       models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='appointment')
    # Accepts full or partial
    status          = models.CharField(max_length=254)
    commission_charges          = models.PositiveIntegerField()
    service_charges          = models.PositiveIntegerField()
    net_charges          = models.PositiveIntegerField()

