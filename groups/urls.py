from django.urls import path
from .views import *

app_name = "groups"

urlpatterns = [
    path('', grouphome.as_view(),name='home')
]
