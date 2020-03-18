from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from polymorphic.models import PolymorphicModel
from django import forms
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

class Group(models.Model):
    admin=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description=models.CharField(max_length=1000)
    members = models.ManyToManyField(User,
                                     through="GroupMember",
                                     through_fields=("group_id", "user_id"),
                                     related_name="groops")
    

class GroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields=['name','description']
    


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Service(PolymorphicModel):
    group_ids = models.CharField(validators=[validate_comma_separated_integer_list],
                                 max_length=200, blank=True, null=True, default='')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="%(class)s_services")
    initiator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    slackness = models.DurationField()
    description = models.CharField(null=False, max_length=1000)  # this is a general description
    stype = models.CharField(null=False, max_length=255)  # one among ['Food','Travel','Shopping']
    members = models.ManyToManyField(User,
                                     through="ServiceMember",
                                     through_fields=("service_id", "user_id"),
                                     related_name="%(class)s_services")


class TravelService(Service):
    start_point = models.CharField(null=False, max_length=1000)
    end_point = models.CharField(null=False, max_length=1000)


class FoodService(Service):
    vendor = models.CharField(null=False, max_length=1000)


class ShoppingService(Service):
    vendor = models.CharField(null=False, max_length=1000)


class ServiceMember(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Message(models.Model):
    timestamp = models.DateTimeField(null=False, auto_now=True)
    content = models.CharField(default='', max_length=1000)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="messages")

# Create your models here.