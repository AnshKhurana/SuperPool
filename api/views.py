from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from pool.models import *
from django.db.models import Q
from datetime import datetime
from pytz import timezone
from django.contrib.postgres.search import SearchVector
from django.http.response import JsonResponse


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

        if 'text' in self.request.GET:
            text = self.request.GET.get('text')
            filt = (Q(description__search=text) | Q(foodservice__vendor__name__search=text)) & filt
        
        return Service.objects.filter(filt).distinct().all()


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

        if 'text' in self.request.GET:
            text = self.request.GET.get('text')
            filt = (Q(description__search=text) | Q(shoppingservice__vendor__name__search=text)) & filt

        return Service.objects.filter(filt).distinct().all()


class TravelServiceList(generics.ListAPIView):
    serializer_class = TravelServiceSerializer

    def get_queryset(self):
        NEARNESS_EPSILON = 5
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt = Q(groups__id__in=gids) & Q(groups__members=user.id)
        print(self.request.GET.keys())

        services = TravelService.objects.all()
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))
        if 'start_point' in self.request.GET and 'end_point' in self.request.GET:
            start_point_id = self.request.GET.get('start_point')
            end_point_id = self.request.GET.get('end_point')
            start_point = Location.objects.get(id=start_point_id)
            end_point = Location.objects.get(id=end_point_id)
            near_start = Location.objects.annotate(radius_sqr=pow(models.F('latitude') - start_point.latitude, 2) + \
                                                              pow(models.F('longitude') - start_point.longitude, 2)). \
                filter(radius_sqr__lte=NEARNESS_EPSILON)
            print('start_points')
            print(near_start)
            near_end = Location.objects.annotate(radius_sqr=pow(models.F('latitude') - end_point.latitude, 2) + \
                                                            pow(models.F('longitude') - end_point.longitude, 2)). \
                filter(radius_sqr__lte=NEARNESS_EPSILON)
            print('end_points')
            print(near_end)
            services = services.filter(start_point__in=near_start, end_point__in=near_end)
        if 'transport' in self.request.GET:
            transport = self.request.GET.get('transport')
            filt = filt & Q(transport=transport)

        if 'text' in self.request.GET:
            text = self.request.GET.get('text')
            filt = (Q(description__search=text) | Q(transport__search=text) |
                    Q(start_point__address__search=text) |
                    Q(end_point__address__search=text)) & filt

        return services.filter(filt).distinct().all()


class EventServiceList(generics.ListAPIView):
    serializer_class = EventServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt = Q(groups__id__in=gids) & Q(category__name='Event') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))

        if 'text' in self.request.GET:
            text = self.request.GET.get('text')
            filt = (Q(description__search=text) |
                    Q(eventservice__location__address__search=text)) & filt

        return Service.objects.filter(filt).distinct().all()


class OtherServiceList(generics.ListAPIView):
    serializer_class = OtherServiceSerializer

    def get_queryset(self):
        user = self.request.user
        gids = self.request.GET.get('gids').split(',')
        filt = Q(groups__id__in=gids) & Q(category__name='Other') & Q(groups__members=user.id)
        if 'start' in self.request.GET and 'end' in self.request.GET:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            filt = filt & Q(start_time__range=(start, end))

        if 'text' in self.request.GET:
            text = self.request.GET.get('text')
            filt = Q(description__search=text) & filt

        return Service.objects.filter(filt).distinct().all()


class FoodServiceReco(generics.ListAPIView):
    serializer_class = FoodServiceSerializer

    def get_queryset(self):
        print('In FoodReco')
        user = self.request.user
        # gids = self.request.GET.get('gids').split(',')
        prev_filt = (Q(initiator=user) | Q(id__in=ServiceMember.objects.filter(user=user).values('service'))) \
                    & Q(start_time__range=(datetime(2000, 1, 1), datetime.now()))
        print('filt made')
        prev_vendors = FoodService.objects.filter(prev_filt).values('vendor')
        print(prev_vendors)
        groups_containing_user = Group.objects.filter(members=user)
        print(groups_containing_user)
        current_filt = Q(groups__id__in=groups_containing_user) & Q(vendor__in=prev_vendors) & \
                       ~Q(initiator=user) & Q(is_active=True) & \
                       ~Q(id__in=ServiceMember.objects.filter(user=user).values('service')) & \
                       Q(end_time__range=(datetime.now(), datetime(3000, 1, 1)))
        print('final filt made')

        return FoodService.objects.filter(current_filt).all()


class ShoppingServiceReco(generics.ListAPIView):
    serializer_class = ShoppingServiceSerializer

    def get_queryset(self):
        print('In ShoppingReco')
        user = self.request.user
        # gids = self.request.GET.get('gids').split(',')
        prev_filt = (Q(initiator=user) | Q(id__in=ServiceMember.objects.filter(user=user).values('service'))) \
                    & Q(start_time__range=(datetime(2000, 1, 1), datetime.now()))
        print('filt made')
        prev_vendors = ShoppingService.objects.filter(prev_filt).values('vendor')
        print(prev_vendors)
        groups_containing_user = Group.objects.filter(members=user)
        print(groups_containing_user)
        current_filt = Q(groups__id__in=groups_containing_user) & Q(vendor__in=prev_vendors) & \
                       ~Q(initiator=user) & Q(is_active=True) & \
                       ~Q(id__in=ServiceMember.objects.filter(user=user).values('service')) & \
                       Q(end_time__range=(datetime.now(), datetime(3000, 1, 1)))
        print('final filt made')

        return ShoppingService.objects.filter(current_filt).all()


class TravelServiceReco(generics.ListAPIView):
    serializer_class = TravelServiceSerializer

    def get_queryset(self):
        print('In TravelReco')
        user = self.request.user
        # gids = self.request.GET.get('gids').split(',')
        prev_filt = (Q(initiator=user) | Q(id__in=ServiceMember.objects.filter(user=user).values('service'))) \
                    & Q(start_time__range=(datetime(2000, 1, 1), datetime.now()))
        print('filt made')
        prev_dest1 = TravelService.objects.filter(prev_filt).values('start_point')
        prev_dest2 = TravelService.objects.filter(prev_filt).values('end_point')
        groups_containing_user = Group.objects.filter(members=user)
        print(groups_containing_user)
        current_filt = Q(groups__id__in=groups_containing_user) & \
                       (Q(start_point__in=prev_dest1) | Q(start_point__in=prev_dest2)) & \
                       ~Q(initiator=user) & Q(is_active=True) & \
                       ~Q(id__in=ServiceMember.objects.filter(user=user).values('service')) & \
                       Q(end_time__range=(datetime.now(), datetime(3000, 1, 1)))
        print('final filt made')

        return TravelService.objects.filter(current_filt).all()


def get_coordinates(request):
    # user = request.user
    pid = request.GET.get('pid')
    # filt = Q(groups__id__in=gids) & Q(category__name='Food') & Q(groups__members=user.id)
    # if 'start' in request.GET and 'end' in self.request.GET:
    #     start = self.request.GET.get('start')
    #     end = self.request.GET.get('end')
    #     filt = filt & Q(start_time__range=(start, end))
    print("pid is " + str(pid))
    print("Location is ")
    z = Location.objects.get(id=pid)
    return JsonResponse({'lat': z.latitude, 'lon': z.longitude})
