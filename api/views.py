from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from pool.models import *
from django.db.models import Q

# Create your views here.
class FoodServiceList(generics.ListAPIView):

    serializer_class = FoodServiceSerializer

    def get_queryset(self):
        # user = self.request.user
        # if user is None:
        #     print("empty user")
        #
        # # return FoodService.objects.all()
        # gids = self.request.GET.get('gids').split(',')
        # print("my statement", gids, user.first_name)
        # return FoodService.objects.filter(groups__pk__in=gids, groups__members=user).all()
        # return FoodService.objects.filter(groups__pk=2).distinct().all()
        # gp = Group.objects.filter(name='g1')
        return Service.objects.filter(Q(groups__name='g2') & Q(category__name='Food')).all()
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


