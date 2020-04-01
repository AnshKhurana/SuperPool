from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from notifications.signals import notify

from pool.models import *
from django.views.generic.base import TemplateView


# Create your views here.


class ActivitiesHome(TemplateView):
    template_name = "activities/activitylist.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ActivitiesHome, self).get_context_data(*args, **kwargs)
        context["groups"] = Group.objects.filter(members=self.request.user.id).all()
        context["gid_string"] = ",".join([str(group.id) for group in context["groups"]])
        context["message"] = -1

        return context


def service_join(request, service_id):
    print(' In activities/views.py  --- service_join ----')
    joinee = request.user
    service = Service.objects.get(id=service_id)
    members = ServiceMember.objects.filter(service=service).values('user')

    if joinee in members:
        return render(request, "activities/activitylist.html", {'message': 0})  # Already in service
    else:
        sm = ServiceMember(service=service, user=joinee)
        sm.save()
        for member in members:
            notify.send(joinee, recipient=User.objects.get(id=member['user']),
                        verb=joinee.username + ' has joined ' + service.description, description=service.category)
        return render(request, "activities/activitylist.html", {'message': 1})  # Joined in service
