from django.urls import include, path, re_path
from django.conf.urls import  url
from .views import *
from rest_framework import routers

app_name = "api"




router= routers.DefaultRouter()
router.register("food/search", FoodSearchView, base_name="food-search")

urlpatterns = [
    re_path(r'^foodservice$', FoodServiceList.as_view(), name='foodservice'),
    re_path(r'^travelservice$',TravelServiceList.as_view(), name = 'travelservice'),
    re_path(r'^shoppingservice$',ShoppingServiceList.as_view(), name = 'shoppingservice'),
    url(r"api/v1/", include(router.urls)),
]

