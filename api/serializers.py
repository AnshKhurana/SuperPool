from pool.models import FoodService, TravelService, ShoppingService, EventService, OtherService
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
        fields = ['start_time', 'end_time', 'initiator', 'description', 'start_point', 'end_point', 'transport']

class ShoppingServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ShoppingService
        fields = ['start_time', 'end_time', 'initiator', 'description', 'vendor']


class EventServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EventService
        fields = ['start_time', 'end_time', 'initiator', 'description', 'location', 'event_type']


class OtherServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OtherService
        fields = ['start_time', 'end_time', 'initiator', 'description']

# class ServiceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ShoppingService
#         fields = ['category','initiator', 'start_time', 'end_time', 'slackness', 'description']
