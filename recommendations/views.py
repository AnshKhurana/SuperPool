from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from notifications.signals import notify

from pool.models import *
from django.views.generic.base import TemplateView


# Create your views here.


class RecommendationsHome(TemplateView):
    template_name = "recommendations/recommendations.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(RecommendationsHome, self).get_context_data(*args, **kwargs)
    #     context["groups"] = Group.objects.filter(members=self.request.user.id).all()
    #     context["gid_string"] = ",".join([str(group.id) for group in context["groups"]])
    #     context["message"] = -1
    #
    #     return context