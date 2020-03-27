from django.urls import path
from .views import FoodCreateView, TravelCreateView, ShoppingCreateView, GroupSelectView, FoodVendorAutocomplete, ShoppingVendorAutocomplete

app_name = "services"

urlpatterns = [
    # path('create', ServiceCreateView.as_view(), name="create"),
    path('foodcreate', FoodCreateView.as_view(), name="foodcreate"),
    path('shoppingcreate', ShoppingCreateView.as_view(), name="shoppingcreate"),
    path('travelcreate', TravelCreateView.as_view(), name="travelcreate"),
    path('groupselect', GroupSelectView.as_view(), name="groupselect"),
    path('food_autocomplete/', FoodVendorAutocomplete.as_view(), name='food-autocomplete'),
    path('shopping_autocomplete/', ShoppingVendorAutocomplete.as_view(), name='shopping-autocomplete'),
]
