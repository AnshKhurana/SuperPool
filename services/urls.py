from django.urls import path
from .views import FoodCreateView

app_name = "services"

urlpatterns = [
    # path('create', ServiceCreateView.as_view(), name="create"),
    path('foodcreate', FoodCreateView.as_view(), name="foodcreate"),
]
