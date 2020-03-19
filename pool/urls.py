from django.urls import path
from .views import *

app_name = "pool"

urlpatterns = [
    # path('create', ServiceCreateView.as_view(),name='create')
    path('', home, name='home')
]
