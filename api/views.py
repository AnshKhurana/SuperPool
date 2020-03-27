from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from pool.models import *
from django.db.models import Q

# Create your views here.
class FoodServiceList(generics.ListAPIView):

    serializer_class = FoodServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt= Q(groups__id__in=gids) & Q(category__name='Food') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start= self.request.GET.get('start')
            end= self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))
        return Service.objects.filter(filt).all()

class TravelServiceList(generics.ListAPIView):

    serializer_class = TravelServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt= Q(groups__id__in=gids) & Q(category__name='Food') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start= self.request.GET.get('start')
            end= self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))
        return Service.objects.filter(filt).all()

class ShoppingServiceList(generics.ListAPIView):

    serializer_class = ShoppingServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt= Q(groups__id__in=gids) & Q(category__name='Food') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start= self.request.GET.get('start')
            end= self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))
        return Service.objects.filter(filt).all()

