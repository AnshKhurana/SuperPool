from django.urls import path
from .views import *

app_name = "pool"

urlpatterns = [
    path('', home, name="home"),
]
