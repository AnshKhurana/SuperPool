"""superpool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from dal import autocomplete
from django.urls import path
from pool.models import FoodVendor
from main_interface.views import FoodVendorAutocomplete, FoodVendorCreateView, FoodVendorUpdateView, ServiceView, GroupCreate, group_join

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_page/', ServiceView.as_view(), name='foodservice_view'),
    path('group_create/', GroupCreate.as_view(), name='groupcreate_view'),
    path('group_join/<int:hash>/', group_join, name='groupjoin_view'),
    path('food_autocomplete/', FoodVendorAutocomplete.as_view(), name='food-autocomplete'),
    path('main_page/add/', FoodVendorCreateView.as_view(), name='foodvendor_create'),
    path('main_page/update/', FoodVendorUpdateView.as_view(), name='foodvendor_update'),
]
# autocomplete.Select2QuerySetView.as_view(model=FoodVendor)