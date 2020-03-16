from django.db import models

# Create your models here.

gmaps_api_key = "AIzaSyAEdRHs5qFXBpXu3HkQXcRXnwBzSbiYZv4"

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=50,
        unique=True,
        help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    ) #

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)

    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    phone_number = PhoneNumberField(null=False, blank=False, unique=True, error_messages=dict(
        unique="A user with that phone number already exists."))

    # any string description
    about = models.TextField(blank=True)

    # location specs




    # # Status for terms and conditions, enforce in HTML
    # tc_status = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "gender"]

    def __unicode__(self):
        return self.email
