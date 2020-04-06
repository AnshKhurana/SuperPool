from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from pool.models import Group

app_name = "recommendations"

urlpatterns = [
    path('', RecommendationsHome.as_view(), name='home'),
]
