from django.db import models

# Create your models here.

gcp_api_key = "AIzaSyAEdRHs5qFXBpXu3HkQXcRXnwBzSbiYZv4"


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

    # first_name and last_name are attributes in AbstractUser

    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    phone_number = PhoneNumberField(null=False, blank=False, unique=True, error_messages=dict(
        unique="A user with that phone number already exists."))

    # any string description
    about = models.TextField(blank=True)

    # location specs

    address = models.CharField(max_length=1000, blank=False, null=False)

    # @Pranay add code to convert addr into internal repr

    # add code here


    # # Status for terms and conditions, enforce in HTML
    # tc_status = models.BooleanField(default=False)

    # USERNAME_FIELD = "email" # we wish to keep the default username scenario
    # REQUIRED_FIELDS = ["username", "gender"] # removed gender

    def __unicode__(self):
        return self.email
