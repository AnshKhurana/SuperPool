from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "chat"

urlpatterns = [
    path('', index, name='home'),
]
