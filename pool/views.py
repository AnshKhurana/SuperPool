from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q

from chat.views import food_index_internal


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('accounts:login'))

    data_kwargs = food_index_internal(request)
    data_kwargs["message"] = -1
    return redirect('chat/food', data_kwargs)
