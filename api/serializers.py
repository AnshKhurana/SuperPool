from pool.models import FoodService, TravelService, ShoppingService, Service
from rest_framework import serializers

class FoodServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodService
        fields = ['start_time', 'end_time', 'slackness', 'description', 'vendor']

class TravelServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TravelService
        fields = ['start_time', 'end_time', 'slackness', 'description', 'start_point', 'end_point']

class ShoppingServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShoppingService
        fields = ['start_time', 'end_time', 'slackness', 'description', 'vendor']


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShoppingService
        fields = ['category','initiator', 'start_time', 'end_time', 'slackness', 'description']
