from django.urls import path
from .views import *

app_name = "services"

urlpatterns = [
    path('create', ServiceCreateView.as_view(), name="create"),

]
