from pool.models import FoodService, TravelService, ShoppingService, Service
from rest_framework import serializers
from accounts.models import *

class FoodServiceSerializer(serializers.HyperlinkedModelSerializer):

    initiator = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FoodService
        fields = ['start_time', 'end_time', 'initiator', 'description', 'vendor']


class TravelServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TravelService
        fields = ['start_time', 'end_time', 'initiator', 'description', 'start_point', 'end_point']

class ShoppingServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ShoppingService
        fields = ['start_time', 'end_time', 'initiator', 'description', 'vendor']


# class ServiceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ShoppingService
#         fields = ['category','initiator', 'start_time', 'end_time', 'slackness', 'description']
