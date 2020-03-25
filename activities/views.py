from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from pool.models import *
from django.views.generic.base import TemplateView

# Create your views here.


class ActivitiesHome(TemplateView):

    template_name ="activities/activitylist.html"

    def get_context_data(self, *args, **kwargs):
        context= super(ActivitiesHome, self).get_context_data(*args, **kwargs)
        context["groups"] = Group.objects.filter(members=self.request.user).all()
        context["gid_string"] = ",".join([str(group.id) for group in context["groups"]])

        return context

