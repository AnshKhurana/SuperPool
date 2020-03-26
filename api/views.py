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
        return Service.objects.filter(Q(groups__id__in=gids) & Q(category__name='Food') & Q(groups__members=user.id)).all()

class TravelServiceList(generics.ListAPIView):

    serializer_class = TravelServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        return Service.objects.filter(Q(groups__id__in=gids) & Q(category__name='Travel') & Q(groups__members=user.id)).all()

class ShoppingServiceList(generics.ListAPIView):

    serializer_class = ShoppingServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        return Service.objects.filter(Q(groups__id__in=gids) & Q(category__name='Shopping') & Q(groups__members=user.id)).all()

