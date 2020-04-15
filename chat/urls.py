from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "chat"

urlpatterns = [
    path('food', food_index, name='home'),
    path('shopping', shopping_index, name='shopping'),
    path('travel', travel_index, name='travel'),
    path('event', event_index, name='event'),
    path('other', other_index, name='other'),
    path('active/<int:service_id>', after_disable, name='active')
]
