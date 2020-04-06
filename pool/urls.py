from django.urls import path
from .views import *
from chat.views import index

app_name = "pool"

urlpatterns = [
    # path('create', ServiceCreateView.as_view(),name='create')
    # path('', home, name='home')
    path('', index, name='home')    # Making My Services the home page
]
