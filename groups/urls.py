from django.urls import path
from .views import *

app_name = "groups"

urlpatterns = [
    path('', grouphome.as_view(), name='home'),
    path('create', GroupCreateView.as_view(), name='create'),
    path('join/<int:hash>', group_join, name='join')
]
