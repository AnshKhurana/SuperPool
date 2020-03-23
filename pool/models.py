from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from polymorphic.models import PolymorphicModel
from django import forms
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)


class Group(models.Model):
    admin = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, default='')
    hash = models.IntegerField(default=0)
    members = models.ManyToManyField(User,
                                     through="GroupMember",
                                     through_fields=("group", "user"),
                                     related_name="groops")

    def __str__(self):
        return f'{self.name}'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)


class Service(PolymorphicModel):
    # group_ids = models.CharField(validators=[validate_comma_separated_integer_list],
    #                              max_length=200, blank=True, null=True, default='')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="%(class)s_services")
    initiator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    slackness = models.DurationField(null=True)
    description = models.CharField(null=False, max_length=1000)  # this is a general description
    # stype = models.CharField(null=False, max_length=255)  # one among ['Food','Travel','Shopping']
    members = models.ManyToManyField(User,
                                     through="ServiceMember",
                                     through_fields=("service_id", "user_id"),
                                     related_name="service_member")

    def __str__(self):
        return self.description

    def get_members(self):
        return "\n".join([p.products for p in self.members.all()])

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id


class ServiceGroup(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

class TravelService(Service):
    start_point = models.CharField(null=False, max_length=1000)
    end_point = models.CharField(null=False, max_length=1000)


class FoodService(Service):
    vendor = models.CharField(null=False, max_length=1000)


class ShoppingService(Service):
    vendor = models.CharField(null=False, max_length=1000)


class ServiceMember(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)


class Message(models.Model):
    timestamp = models.DateTimeField(null=False, auto_now=True)
    content = models.CharField(default='', max_length=1000)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="messages")

# Create your models here.
