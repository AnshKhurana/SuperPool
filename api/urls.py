from django.urls import include, path, re_path
from .views import *
from rest_framework import routers

app_name = "api"

router= routers.DefaultRouter()
urlpatterns = [
    re_path(r'^foodservice$', FoodServiceList.as_view(), name='foodservice'),
    re_path(r'^travelservice$',TravelServiceList.as_view(), name = 'travelservice'),
    re_path(r'^shoppingservice$',ShoppingServiceList.as_view(), name = 'shoppingservice'),
]
