from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from notifications.signals import notify
from django.views.generic import FormView, CreateView
from pool.models import *
from .forms import *
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core import serializers
from dal import autocomplete
import subprocess
import requests
from datetime import datetime
from django.conf import settings


# Create your views here.

# class FoodCreateView(LoginRequiredMixin, FormView):
#     form_class= FoodCreationForm
#     success_url = '/'
#     template_name = 'services/foodcreate.html'
#
#     def form_valid(self, form):
#         form.save(self.request.user)
#         return super().form_valid(form)


class FoodCreateView(LoginRequiredMixin, CreateView):
    form_class = FoodCreationForm
    template_name = 'services/integrated_create.html'
    success_url = '/'

    def form_valid(self, form):
        if not ('servicegroups' in self.request.session):
            form.add_error(None, "Session expired")
            return super().form_invalid(form)
        else:
            groups = self.request.session['servicegroups']
            del self.request.session['servicegroups']

        u = self.request.user
        data = form.save()
        f = FoodService(category=Category.objects.get(name='Food'), initiator=u, vendor=data['vendor'],
                        description=data['description'],
                        start_time=data['start_time'], end_time=data['end_time'],
                        )
        f.save()
        sm = ServiceMember(service=f, user=u)
        sm.save()

        notified_members = set()
        for group in serializers.deserialize("json", groups):
            gs = ServiceGroup(group=group.object, service=f)
            gs.save()

            members = GroupMember.objects.filter(group=group.object).values('user')
            print(members)
            for member in members:
                print(member)
                notified_members.add(User.objects.get(id=member['user']))

        # for member in notified_members:
        #     notify.send(self.request.user, recipient=member, verb=data['description'], description="Food " + str(f.id))

        # form.save(self.request.user)
        return render(self.request, "home.html", {'message': 2})


class ShoppingCreateView(LoginRequiredMixin, FormView):
    form_class = ShoppingCreationForm
    success_url = '/'
    template_name = 'services/shoppingcreate.html'

    def form_valid(self, form):
        if not ('servicegroups' in self.request.session):
            form.add_error(None, "Session expired")
            return super().form_invalid(form)
        else:
            groups = self.request.session['servicegroups']
            del self.request.session['servicegroups']

        u = self.request.user
        data = form.save()
        f = ShoppingService(category=Category.objects.get(name='Shopping'), initiator=u, vendor=data['vendor'],
                            description=data['description'],
                            start_time=data['start_time'], end_time=data['end_time'],
                            )
        f.save()
        sm = ServiceMember(service=f, user=u)
        sm.save()
        for group in serializers.deserialize("json", groups):
            gs = ServiceGroup(group=group.object, service=f)
            gs.save()
        # form.save(self.request.user)
        return render(self.request, "home.html", {'message': 3})


class TravelCreateView(LoginRequiredMixin, FormView):
    form_class = TravelCreationForm
    success_url = '/'
    template_name = 'services/travelcreate.html'

    def form_valid(self, form):
        if not ('servicegroups' in self.request.session):
            form.add_error(None, "Session expired")
            return super().form_invalid(form)
        else:
            groups = self.request.session['servicegroups']
            del self.request.session['servicegroups']
        u = self.request.user
        data = form.save()
        print('Form data obtained')
        f = TravelService(category=Category.objects.get(name='Travel'), initiator=u, start_point=data["start_point"],
                          end_point=data["end_point"], description=data['description'],
                          start_time=data['start_time'], end_time=data['end_time'], transport=data['transport'],

                          )
        f.save()
        print('TravelService saved')
        sm = ServiceMember(service=f, user=u)
        sm.save()
        print('ServiceMember saved')
        for group in serializers.deserialize("json", groups):
            gs = ServiceGroup(group=group.object, service=f)
            gs.save()
        print('ServiceGroups registered')
        # form.save(self.request.user)
        return render(self.request, "home.html", {'message': 4})


class EventCreateView(LoginRequiredMixin, FormView):
    form_class = EventCreationForm
    success_url = '/'
    template_name = 'services/eventcreate.html'

    def form_valid(self, form):
        if not ('servicegroups' in self.request.session):
            form.add_error(None, "Session expired")
            return super().form_invalid(form)
        else:
            groups = self.request.session['servicegroups']
            del self.request.session['servicegroups']

        u = self.request.user
        data = form.save()
        f = EventService(category=Category.objects.get(name='Event'), initiator=u, description=data['description'],
                         start_time=data['start_time'], end_time=data['end_time'], slackness=data['slackness'],
                         location=data['location'], event_type=data['event_type'],
                         )
        f.save()
        sm = ServiceMember(service=f, user=u)
        sm.save()
        for group in serializers.deserialize("json", groups):
            gs = ServiceGroup(group=group.object, service=f)
            gs.save()
        # form.save(self.request.user)
        return render(self.request, "home.html", {'message': 5})


class OtherCreateView(LoginRequiredMixin, FormView):
    form_class = OtherCreationForm
    success_url = '/'
    template_name = 'services/othercreate.html'

    def form_valid(self, form):
        if not ('servicegroups' in self.request.session):
            form.add_error(None, "Session expired")
            return super().form_invalid(form)
        else:
            groups = self.request.session['servicegroups']
            del self.request.session['servicegroups']

        u = self.request.user
        data = form.save()
        f = OtherService(category=Category.objects.get(name='Other'), initiator=u, description=data['description'],
                         start_time=data['start_time'], end_time=data['end_time'], slackness=data['slackness'],
                         )
        f.save()
        sm = ServiceMember(service=f, user=u)
        sm.save()
        for group in serializers.deserialize("json", groups):
            gs = ServiceGroup(group=group.object, service=f)
            gs.save()
        # form.save(self.request.user)
        return render(self.request, "home.html", {'message': 6})


class GroupSelectView(LoginRequiredMixin, FormView):
    form_class = GroupSelectForm
    success_url = reverse_lazy('create')
    template_name = 'services/groupselect.html'

    def get_success_url(self):
        if 'Food' in self.request.POST:
            return reverse_lazy('services:foodcreate')
        elif 'Shopping' in self.request.POST:
            return reverse_lazy('services:shoppingcreate')
        elif 'Travel' in self.request.POST:
            return reverse_lazy('services:travelcreate')
        elif 'Event' in self.request.POST:
            return reverse_lazy('services:eventcreate')
        else:
            return reverse_lazy('services:othercreate')

    def get_form_kwargs(self):
        kwargs = super(GroupSelectView, self).get_form_kwargs()
        kwargs['currentuser'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.request.session['servicegroups'] = serializers.serialize("json", form.cleaned_data['groups'].all(),
                                                                      fields=())
        return super().form_valid(form)


class FoodVendorAutocomplete(autocomplete.Select2QuerySetView):
    # model = FoodVendor
    # context_object_name = 'Food Vendor'
    # template_name = 'pool/foodvendor_form.html'

    def get_queryset(self):
        qs = Restaurant.objects.all()
        if self.q:
            qs = qs.filter(name__contains=self.q)
        # print(qs)
        return qs


class ShoppingVendorAutocomplete(autocomplete.Select2QuerySetView):
    # model = FoodVendor
    # context_object_name = 'Food Vendor'
    # template_name = 'pool/foodvendor_form.html'

    def get_queryset(self):
        current_time = datetime.now()
        if self.q:
            responses = requests.get(settings.COMPANY_API_URL, params={'query': self.q}).json()
            for response in responses:
                company = Company(name=response['name'],
                                  domain=response['domain'],
                                  logo=response['logo'],
                                  timestamp=current_time)
                company.save()
        qs = Company.objects.filter(timestamp=current_time)
        # print(qs)
        return qs


class LocationAutocomplete(autocomplete.Select2QuerySetView):
    # model = FoodVendor
    # context_object_name = 'Food Vendor'
    # template_name = 'pool/foodvendor_form.html'

    def get_queryset(self):
        url = "https://us1.locationiq.com/v1/autocomplete.php"
        KEY = 'c635736cc00334'
        COUNTRY_CODE = 'in'
        LIMIT = 15
        current_time = datetime.now()
        if self.q:
            data = {
                'key': KEY,
                'q': self.q,
                'countrycodes': COUNTRY_CODE,
                'limit': LIMIT,
                'format': 'json'
            }
            responses = requests.get(url, params=data).json()
            for response in responses:
                print(response.keys())
                if 'error' in response.keys():
                    break
                location = Location(latitude=response['lat'],
                                    longitude=response['lon'],
                                    address=response['display_address'],
                                    timestamp=current_time)
                location.save()
        qs = Location.objects.filter(timestamp=current_time)
        print(qs)
        return qs

# @login_required
# class ServiceCreateView(FormView):
#
#     # model = Service
#     form_class = ServiceCreationForm
#     success_url = '/'
#     template_name = 'services/create.html'
#
#
#     def get_success_url(self):
#         return self.success_url
#
#     def post(self, request, *args, **kwargs):
#
#         service_create_form = ServiceCreationForm(data=request.POST)
#
#         if service_create_form.is_valid():
#             service_create_form.save(commit=True)
#             return redirect('pool:home')
#         else:
#             print(service_create_form.errors)
#             return render(request, 'services/create.html', {'form_cat': service_create_form})
#
#
#     # fields=['name','description']
#
#     # # def get_initial(self):
#     # #     initial=super(GroupCreateView,self).get_initial()
#     # #     initial['admin_id']=self.request.user.id
#     # #     return initial
#     # def form_valid(self, form):
#     #     form.instance.admin=User.objects.get(id=self.request.user.id)
#     #     return super(GroupCreateView,self).form_valid(form)
