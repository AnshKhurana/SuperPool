from pool.models import FoodService, TravelService, ShoppingService, Service
from rest_framework import serializers
from pool.models import ServiceMember
from accounts.models import *


class FoodServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)
    my_field = serializers.SerializerMethodField('am_i_there')

    def am_i_there(self, foodservice):
        print('FoodService')
        cur_user = self.context['request'].user
        service_initiator = foodservice.initiator
        service_members = User.objects.filter(id__in=ServiceMember.objects.filter(service=foodservice).values('user'))
        return cur_user == service_initiator or cur_user in service_members

    class Meta:
        model = FoodService
        fields = ['id', 'start_time', 'end_time', 'initiator', 'description', 'vendor', 'my_field', 'is_active']


class ShoppingServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)
    my_field = serializers.SerializerMethodField('am_i_there')

    def am_i_there(self, shoppingservice):
        print('ShoppingService')
        cur_user = self.context['request'].user
        service_initiator = shoppingservice.initiator
        service_members = User.objects.filter(id__in=ServiceMember.objects.filter(service=shoppingservice).values('user'))
        return cur_user == service_initiator or cur_user in service_members

    class Meta:
        model = ShoppingService
        fields = ['id', 'start_time', 'end_time', 'initiator', 'description', 'vendor', 'my_field', 'is_active']


class TravelServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)
    my_field = serializers.SerializerMethodField('am_i_there')

    def am_i_there(self, travelservice):
        print('TravelService')
        cur_user = self.context['request'].user
        service_initiator = travelservice.initiator
        service_members = User.objects.filter(id__in=ServiceMember.objects.filter(service=travelservice).values('user'))
        return cur_user == service_initiator or cur_user in service_members

    class Meta:
        model = TravelService
        fields = ['id', 'start_time', 'end_time', 'initiator', 'description', 'start_point', 'end_point', 'my_field', 'is_active']

# class ServiceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ShoppingService
#         fields = ['category','initiator', 'start_time', 'end_time', 'slackness', 'description']
