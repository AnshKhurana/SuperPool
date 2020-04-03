from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from pool.models import *
from django.db.models import Q
from datetime import datetime
from pytz import timezone


# Create your views here.
class FoodServiceList(generics.ListAPIView):
    serializer_class = FoodServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt = Q(groups__id__in=gids) & Q(category__name='Food') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))
        return Service.objects.filter(filt).all()


class ShoppingServiceList(generics.ListAPIView):
    serializer_class = ShoppingServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt = Q(groups__id__in=gids) & Q(category__name='Shopping') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))
        return Service.objects.filter(filt).all()


class TravelServiceList(generics.ListAPIView):
    serializer_class = TravelServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt = Q(groups__id__in=gids) & Q(category__name='Travel') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))
        return Service.objects.filter(filt).all()


class FoodServiceReco(generics.ListAPIView):
    serializer_class = FoodServiceSerializer

    def get_queryset(self):
        print('In FoodReco')
        user = self.request.user
        # gids = self.request.GET.get('gids').split(',')
        prev_filt = (Q(initiator=user) | Q(id__in=ServiceMember.objects.filter(user=user).values('service'))) \
                    & Q(start_time__range=(datetime(2000, 1, 1), datetime.now(timezone('Asia/Kolkata'))))
        print('filt made')
        prev_vendors = FoodService.objects.filter(prev_filt).values('vendor')
        print(prev_vendors)
        groups_containing_user = Group.objects.filter(members=user)
        print(groups_containing_user)
        current_filt = Q(groups__id__in=groups_containing_user) & Q(vendor__in=prev_vendors) & \
                       ~Q(initiator=user) & Q(is_active=True) & \
                       ~Q(id__in=ServiceMember.objects.filter(user=user).values('service')) & \
                       Q(end_time__range=(datetime.now().astimezone(timezone('Asia/Kolkata')), datetime(3000, 1, 1)))
        print('final filt made')

        return FoodService.objects.filter(current_filt).all()


class ShoppingServiceReco(generics.ListAPIView):
    serializer_class = ShoppingServiceSerializer

    def get_queryset(self):
        print('In ShoppingReco')
        user = self.request.user
        # gids = self.request.GET.get('gids').split(',')
        prev_filt = (Q(initiator=user) | Q(id__in=ServiceMember.objects.filter(user=user).values('service'))) \
                    & Q(start_time__range=(datetime(2000, 1, 1), datetime.now(timezone('Asia/Kolkata'))))
        print('filt made')
        prev_vendors = ShoppingService.objects.filter(prev_filt).values('vendor')
        print(prev_vendors)
        groups_containing_user = Group.objects.filter(members=user)
        print(groups_containing_user)
        current_filt = Q(groups__id__in=groups_containing_user) & Q(vendor__in=prev_vendors) & \
                       ~Q(initiator=user) & Q(is_active=True) & \
                       ~Q(id__in=ServiceMember.objects.filter(user=user).values('service')) & \
                       Q(end_time__range=(datetime.now(timezone('Asia/Kolkata')), datetime(3000, 1, 1)))
        print('final filt made')

        return ShoppingService.objects.filter(current_filt).all()


class TravelServiceReco(generics.ListAPIView):
    serializer_class = TravelServiceSerializer

    def get_queryset(self):
        print('In TravelReco')
        user = self.request.user
        # gids = self.request.GET.get('gids').split(',')
        prev_filt = (Q(initiator=user) | Q(id__in=ServiceMember.objects.filter(user=user).values('service'))) \
                    & Q(start_time__range=(datetime(2000, 1, 1), datetime.now(timezone('Asia/Kolkata'))))
        print('filt made')
        prev_dest1 = TravelService.objects.filter(prev_filt).values('start_point')
        prev_dest2 = TravelService.objects.filter(prev_filt).values('end_point')
        groups_containing_user = Group.objects.filter(members=user)
        print(groups_containing_user)
        current_filt = Q(groups__id__in=groups_containing_user) & \
                       (Q(start_point__in=prev_dest1) | Q(start_point__in=prev_dest2)) & \
                       ~Q(initiator=user) & Q(is_active=True) & \
                       ~Q(id__in=ServiceMember.objects.filter(user=user).values('service')) & \
                       Q(end_time__range=(datetime.now(timezone('Asia/Kolkata')), datetime(3000, 1, 1)))
        print('final filt made')

        return TravelService.objects.filter(current_filt).all()
