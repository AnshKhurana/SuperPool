from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from pool.models import *
from .forms import ServiceCreationForm, ShoppingCreationForm, TravelCreationForm, GroupSelectForm, \
    FoodCreationForm
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
                        start_time=data['start_time'], end_time=data['end_time'], slackness=data['slackness'],
                        )
        f.save()
        sm = ServiceMember(service=f, user=u)
        sm.save()
        for group in serializers.deserialize("json", groups):
            gs = ServiceGroup(group=group.object, service=f)
            gs.save()
        # form.save(self.request.user)
        return super().form_valid(form)


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
                            start_time=data['start_time'], end_time=data['end_time'], slackness=data['slackness'],
                            )
        f.save()
        sm = ServiceMember(service=f, user=u)
        sm.save()
        for group in serializers.deserialize("json", groups):
            gs = ServiceGroup(group=group.object, service=f)
            gs.save()
        # form.save(self.request.user)
        return super().form_valid(form)


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
        f = TravelService(category=Category.objects.get(name='Travel'), initiator=u, start_point=data["start_point"],
                          end_point=data["end_point"], description=data['description'],
                          start_time=data['start_time'], end_time=data['end_time'],
                          slackness=data['slackness']
                          )
        f.save()
        sm = ServiceMember(service=f, user=u)
        sm.save()
        for group in serializers.deserialize("json", groups):
            gs = ServiceGroup(group=group.object, service=f)
            gs.save()
        # form.save(self.request.user)
        return super().form_valid(form)


class GroupSelectView(LoginRequiredMixin, FormView):
    form_class = GroupSelectForm
    success_url = reverse_lazy('create')
    template_name = 'services/groupselect.html'

    def get_success_url(self):
        if 'Food' in self.request.POST:
            return reverse_lazy('services:foodcreate')
        elif 'Shopping' in self.request.POST:
            return reverse_lazy('services:shoppingcreate')
        else:
            return reverse_lazy('services:travelcreate')

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
