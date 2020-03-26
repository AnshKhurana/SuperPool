from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from pool.models import Group

app_name = "groups"

urlpatterns = [
    path('', grouphome.as_view(), name='home'),
    path('display/<slug:pk>', GroupListView.as_view(), name='display'),
    path('remove_member/<int:g_id>/<int:user_id>', remove_member, name='remove_member'),
    path('create', GroupCreateView.as_view(), name='create'),
    path('join/<int:hash>', group_join, name='join')
]
