from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from pool.models import *

# Create your views here.
class FoodServiceList(generics.ListAPIView):

    serializer_class = FoodServiceSerializer

    def get_queryset(self):
        user = self.request.user
        # return FoodService.objects.all()
        gids = self.request.GET.get('gids').split(',')
        # print(gids)
        # return FoodService.objects.filter(groups__pk__in=gids, groups__members=user).all()
        # return FoodService.objects.filter(groups__pk=2).distinct().all()
        return FoodService.objects.filter(groups_pk=2).all()
        # return FoodService.objects.all()

class TravelServiceList(generics.ListAPIView):

    serializer_class = TravelServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        return TravelService.objects.filter(groups__pk__in=gids, groups__members=user).all()

class ShoppingServiceList(generics.ListAPIView):

    serializer_class = ShoppingServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        return ShoppingService.objects.filter(groups__pk__in=gids, groups__members=user).all()


