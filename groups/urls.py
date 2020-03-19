from django.urls import path
from .views import *
from pool.models import Group

app_name = "groups"

urlpatterns = [
    path('', grouphome.as_view(), name='home'),
    path('display/<int:g_id>', GroupListView.as_view(), name='display'),
    path('create', GroupCreateView.as_view(), name='create'),
    path('join/<int:hash>', group_join, name='join')
]
