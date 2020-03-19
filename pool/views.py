from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('accounts:login'))

    return render(request, 'home.html')
