from django.db import models

# Create your models here.

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
    )

    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    phone_number = PhoneNumberField(null=False, blank=False, unique=True, error_messages=dict(
        unique="A user with that email already exists."))

    gender = models.CharField(max_length=20)

    # Status for terms and conditions
    tc_status = models.BooleanField(default=False)

    about = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "gender"]

    def __unicode__(self):
        return self.email
