from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from pool.models import *
from accounts.models import User

# Create your views here.

class ServiceCreateView(CreateView):
    model=Service
    # fields=['name','description']
    # success_url = '/groups'
    # # def get_initial(self):
    # #     initial=super(GroupCreateView,self).get_initial()
    # #     initial['admin_id']=self.request.user.id
    # #     return initial
    # def form_valid(self, form):
    #     form.instance.admin=User.objects.get(id=self.request.user.id)
    #     return super(GroupCreateView,self).form_valid(form)