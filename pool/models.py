from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from polymorphic.models import PolymorphicModel


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name


class User(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name


class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User,
                                     through="GroupMember",
                                     through_fields=("group_id", "user_id"),
                                     related_name="groups")

    def __str__(self):
        return '%s' % self.name


class GroupMember(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s' % self.group_id.name


class FoodVendor(models.Model):
    vendor = models.CharField(null=False, max_length=1000)

    def __str__(self):
        return '%s' % self.vendor


class ShopVendor(models.Model):
    vendor = models.CharField(null=False, max_length=1000)

    def __str__(self):
        return '%s' % self.vendor


class Service(PolymorphicModel):
    group_ids = models.CharField(validators=[validate_comma_separated_integer_list],
                                 max_length=200, blank=True, null=True, default='')
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="%(class)s_services")
    initiator_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    slackness = models.DurationField(null=True)
    description = models.CharField(null=False, max_length=1000)  # this is a general description
    members = models.ManyToManyField(User,
                                     through="ServiceMember",
                                     through_fields=("service_id", "user_id"),
                                     related_name="%(class)s_services")

    def __unicode__(self):
        return self.description


class TravelService(Service):
    start_point = models.CharField(null=False, max_length=1000)
    end_point = models.CharField(null=False, max_length=1000)

    def __unicode__(self):
        return self.start_point


class FoodService(Service):
    vendor = models.ForeignKey(FoodVendor, on_delete=models.DO_NOTHING, null=True)

    def __unicode__(self):
        return self.vendor


class ShoppingService(Service):
    vendor = models.ForeignKey(ShopVendor, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return '%s' % self.vendor


class ServiceMember(models.Model):
    service_id = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Message(models.Model):
    timestamp = models.DateTimeField(null=False, auto_now=True)
    content = models.CharField(default='', max_length=1000)
    service_id = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name="messages")
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="messages")

    def __str__(self):
        return '%s' % self.content


class GroupLink(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    hash = models.IntegerField(default=0)
