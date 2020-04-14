from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from notifications.signals import notify

from activities.forms import TravelActivityForm, FoodActivityForm, ShoppingActivityForm
from pool.models import *
from django.views.generic.base import TemplateView


# Create your views here.


class ActivitiesHome(TemplateView):
    food_form_class = FoodActivityForm
    shopping_form_class = ShoppingActivityForm
    travel_form_class = TravelActivityForm

    template_name = "activities/activitylist.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ActivitiesHome, self).get_context_data(*args, **kwargs)
        # print(context)
        context["groups"] = Group.objects.filter(members=self.request.user.id).all()
        context["gid_string"] = ",".join([str(group.id) for group in context["groups"]])
        context["message"] = -1
        # print('context data created')
        # print(dir(context['view'].food_form_class))
        return context


def service_join(request, service_id):
    print(' In activities/views.py  --- service_join ----')
    joinee = request.user
    service = Service.objects.get(id=service_id)
    members = ServiceMember.objects.filter(service=service).values('user')

    groups = Group.objects.filter(members=request.user.id).all()
    gid_string = ",".join([str(group.id) for group in groups])

    if joinee in members:
        return render(request, "activities/activitylist.html",
                      {'groups': groups, 'gid_string': gid_string, 'message': 0})  # Already in service
    else:
        sm = ServiceMember(service=service, user=joinee)
        sm.save()
        for member in members:
            notify.send(joinee, recipient=User.objects.get(id=member['user']),
                        verb=joinee.username + ' has joined ' + service.description, description=service.category)
        return render(request, "activities/activitylist.html",
                      {'groups': groups, 'gid_string': gid_string, 'message': 1})  # Joined in service
