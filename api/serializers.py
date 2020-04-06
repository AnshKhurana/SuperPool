
from pool.models import FoodService, TravelService, ShoppingService, EventService, OtherService
from django.db.models import Q
from rest_framework import serializers
from pool.models import ServiceMember
from accounts.models import *
from datetime import datetime, timezone as tz
from pytz import timezone


class FoodServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)
    my_field = serializers.SerializerMethodField('am_i_there')
    use_count_field = serializers.SerializerMethodField('use_count')
    time_left_field = serializers.SerializerMethodField('time_left')

    def am_i_there(self, foodservice):
        print('FoodService')
        cur_user = self.context['request'].user
        service_initiator = foodservice.initiator
        service_members = User.objects.filter(id__in=ServiceMember.objects.filter(service=foodservice).values('user'))
        return cur_user == service_initiator or cur_user in service_members

    def use_count(self, foodservice):
        vendor = foodservice.vendor
        cur_user = self.context['request'].user
        filt = Q(initiator=cur_user) & Q(category__name='Food') \
               & Q(start_time__range=(datetime(2000, 1, 1), datetime.now(timezone('Asia/Kolkata')))) & Q(vendor=vendor)
        fs = FoodService.objects.filter(filt)
        print(fs.count())
        return fs.count()

    def time_left(self, foodservice):
        now = datetime.now(tz.utc)
        diff = (foodservice.end_time - now) // 3600
        diff = str(diff).split(':')[2].split('.')[0]
        print(diff)
        return diff

    class Meta:
        model = FoodService
        fields = ['id', 'start_time', 'end_time', 'initiator', 'description', 'vendor', 'my_field', 'is_active', 'use_count_field', 'time_left_field']


class ShoppingServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)
    my_field = serializers.SerializerMethodField('am_i_there')
    use_count_field = serializers.SerializerMethodField('use_count')
    time_left_field = serializers.SerializerMethodField('time_left')

    def am_i_there(self, shoppingservice):
        print('ShoppingService')
        cur_user = self.context['request'].user
        service_initiator = shoppingservice.initiator
        service_members = User.objects.filter(id__in=ServiceMember.objects.filter(service=shoppingservice).values('user'))
        return cur_user == service_initiator or cur_user in service_members

    def use_count(self, foodservice):
        vendor = foodservice.vendor
        cur_user = self.context['request'].user
        filt = Q(initiator=cur_user) & Q(category__name='Food') \
               & Q(start_time__range=(datetime(2000, 1, 1), datetime.now(timezone('Asia/Kolkata')))) & Q(vendor=vendor)
        fs = FoodService.objects.filter(filt)
        print(fs.count())
        return fs.count()

    def time_left(self, foodservice):
        now = datetime.now(tz.utc)
        diff = (foodservice.end_time - now) // 3600
        diff = str(diff).split(':')[2].split('.')[0]
        print(diff)
        return diff

    class Meta:
        model = ShoppingService
        fields = ['id', 'start_time', 'end_time', 'initiator', 'description', 'vendor', 'my_field', 'is_active', 'use_count_field', 'time_left_field']


class TravelServiceSerializer(serializers.HyperlinkedModelSerializer):
    initiator = serializers.StringRelatedField(read_only=True)
    my_field = serializers.SerializerMethodField('am_i_there')
    use_count_field = serializers.SerializerMethodField('use_count')
    time_left_field = serializers.SerializerMethodField('time_left')

    def am_i_there(self, travelservice):
        print('TravelService')
        cur_user = self.context['request'].user
        service_initiator = travelservice.initiator
        service_members = User.objects.filter(id__in=ServiceMember.objects.filter(service=travelservice).values('user'))
        return cur_user == service_initiator or cur_user in service_members

    def use_count(self, foodservice):
        vendor = foodservice.vendor
        cur_user = self.context['request'].user
        filt = Q(initiator=cur_user) & Q(category__name='Food') \
               & Q(start_time__range=(datetime(2000, 1, 1), datetime.now(timezone('Asia/Kolkata')))) & Q(vendor=vendor)
        fs = FoodService.objects.filter(filt)
        print(fs.count())
        return fs.count()

    def time_left(self, foodservice):
        now = datetime.now(tz.utc)
        diff = (foodservice.end_time - now) // 3600
        diff = str(diff).split(':')[2].split('.')[0]
        print(diff)
        return diff

    class Meta:
        model = TravelService
        fields = ['id', 'start_time', 'end_time', 'initiator', 'description', 'start_point', 'end_point', 'my_field', 'is_active', 'use_count_field', 'time_left_field']

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
