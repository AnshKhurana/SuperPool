from django.urls import path
from .views import FoodCreateView, TravelCreateView, ShoppingCreateView

app_name = "services"

urlpatterns = [
    # path('create', ServiceCreateView.as_view(), name="create"),
    path('foodcreate', FoodCreateView.as_view(), name="foodcreate"),
    path('shoppingcreate', ShoppingCreateView.as_view(), name="shoppingcreate"),
    path('travelcreate', TravelCreateView.as_view(), name="travelcreate"),
]
