from django.urls import include, path, re_path
from .views import *
from rest_framework import routers

app_name = "api"

router = routers.DefaultRouter()
urlpatterns = [
    re_path(r'^foodservice$', FoodServiceList.as_view(), name='foodservice'),
    re_path(r'^travelservice$', TravelServiceList.as_view(), name='travelservice'),
    re_path(r'^shoppingservice$', ShoppingServiceList.as_view(), name='shoppingservice'),
    re_path(r'^eventservice$', EventServiceList.as_view(), name='eventservice'),
    re_path(r'^otherservice$', OtherServiceList.as_view(), name='otherservice'),
    re_path(r'^get_coordinates$', get_coordinates, name='get_coordinates'),

    re_path(r'^foodservicereco$', FoodServiceReco.as_view(), name='foodservicereco'),
    re_path(r'^travelservicereco$', TravelServiceReco.as_view(), name='travelservicereco'),
    re_path(r'^shoppingservicereco$', ShoppingServiceReco.as_view(), name='shoppingservicereco'),

]
