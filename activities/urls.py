from django.urls import path
from .views import *

app_name = "activities"

urlpatterns = [
    path('', ActivitiesHome.as_view(), name="act"),
    path('servicejoin/<int:service_id>', service_join, name="service_join"),
]
