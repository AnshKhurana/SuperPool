from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from pool.models import *
from django.db.models import Q

from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet

from pool.search_indexes import FoodIndex

# Create your views here.

class FoodSearchSerializer(HaystackSerializer):

    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [FoodIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "text"
        ]



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

        if 'text'in self.request.GET:
            text = self.request.GET.get('text')


        return Service.objects.filter(filt).all()




class TravelServiceList(generics.ListAPIView):

    serializer_class = TravelServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt= Q(groups__id__in=gids) & Q(category__name='Travel') & Q(groups__members=user.id)
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
        filt= Q(groups__id__in=gids) & Q(category__name='Shopping') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start= self.request.GET.get('start')
            end= self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))
        return Service.objects.filter(filt).all()


class FoodSearchView(HaystackViewSet):

    # `index_models` is an optional list of which models you would like to include
    # in the search result. You might have several models indexed, and this provides
    # a way to filter out those of no interest for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
    index_models = [FoodService]

    serializer_class = FoodSearchSerializer