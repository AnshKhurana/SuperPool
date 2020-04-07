from django.urls import path
from .views import *

app_name = "services"

urlpatterns = [
    # path('create', ServiceCreateView.as_view(), name="create"),
    path('foodcreate', FoodCreateView.as_view(), name="foodcreate"),
    path('shoppingcreate', ShoppingCreateView.as_view(), name="shoppingcreate"),
    path('travelcreate', TravelCreateView.as_view(), name="travelcreate"),
    path('eventcreate', EventCreateView.as_view(), name="eventcreate"),
    path('othercreate', OtherCreateView.as_view(), name="othercreate"),
    path('groupselect', GroupSelectView.as_view(), name="groupselect"),
    path('food_autocomplete/', FoodVendorAutocomplete.as_view(), name='food-autocomplete'),
    path('shopping_autocomplete/', ShoppingVendorAutocomplete.as_view(), name='shopping-autocomplete'),
    path('location_autocomplete/', LocationAutocomplete.as_view(), name='location-autocomplete'),
]
