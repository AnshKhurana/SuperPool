from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from pool.models import Group

app_name = "notification"

urlpatterns = [
    path('', notification_home.as_view(), name='home'),
    path('/mark_as_read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('/mark_all_as_read/', mark_all_as_read, name='mark_all_as_read'),
    path('/join_service/<int:service_id>', join_service, name='join_service_from_notification'),
]
