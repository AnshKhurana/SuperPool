from django.urls import path
from .views import *

app_name = "location"

urlpatterns = [
    path('location_autocomplete/', LocationAutocomplete.as_view(), name='location-autocomplete'),
]
