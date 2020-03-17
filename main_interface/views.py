from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from pool.models import FoodVendor

# Create your views here.

class FoodVendorListView(ListView):
    model = FoodVendor
    context_object_name = 'Food Vendor'

class FoodVendorCreateView(CreateView):
    model = FoodVendor
    fields = ('vendor', )
    success_url = reverse_lazy('foodVendor_changelist')

class FoodVendorUpdateView(UpdateView):
    model = FoodVendor
    fields = ('vendor', )
    success_url = reverse_lazy('foodVendor_changelist')
