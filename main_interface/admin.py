from django.contrib import admin

# Register your models here.
from pool.models import FoodService, FoodVendor
from .forms import FoodServiceForm


class FoodAdmin(admin.ModelAdmin):
    form = FoodServiceForm


admin.site.register(FoodService, FoodAdmin)