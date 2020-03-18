from django.shortcuts import render, redirect
from dal import autocomplete
import random
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from pool.models import FoodVendor, FoodService, Group, GroupMember, User, GroupLink
from .forms import FoodServiceForm, GroupCreateForm

hashmap, hashmap_rev = {}, {}

# Create your views here.

class ServiceView(CreateView):
    model = FoodService
    form_class = FoodServiceForm
    template_name = 'pool/foodvendor_form.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url


class GroupCreate(CreateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'pool/groupcreate_form.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        print("Arnab")
        # if self.request.user.is_authenticated:
        #     return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):

        user_form = GroupCreateForm(data=request.POST)

        if user_form.is_valid():
            print(user_form)
            user = user_form.save()
            print(user.name)
            for q in user.members.all():
                print(q)

            hash = random.getrandbits(32)
            hashmap[user] = hash
            hashmap_rev[hash] = user
            grouplink = GroupLink(group=user, hash=hashmap[user])
            grouplink.save()
            # password = user_form.cleaned_data.get("password1")
            # user.set_password(password)
            # user.save()
            client_ip = request.META['REMOTE_ADDR']
            return HttpResponse("<h>%s</h>" % "http://"+client_ip+":8080/group_join/"+str(hashmap[user]))
        else:
            print(user_form.errors)
            return render(request, 'accounts/register.html', {'form': user_form})


def group_join(request, hash):
    data=request.POST
    print(request)
    print(hash)
    print(data)
    u = User.objects.filter(name='B1')[0]
    print(u)
    group_link = GroupLink.objects.filter(hash=hash)[0]
    print(group_link.group)
    member = GroupMember(group_id=group_link.group, user_id=u)
    member.save()
    print(member)
    return redirect('/main_page/')


class FoodVendorAutocomplete(autocomplete.Select2QuerySetView):
    # model = FoodVendor
    # context_object_name = 'Food Vendor'
    # template_name = 'pool/foodvendor_form.html'

    def get_queryset(self):
        print('Arnab')
        qs = FoodVendor.objects.all()
        # qs = qs.filter(vendor__istartswith='K')
        print('Arnab1')
        # print(qs)
        if self.q:
            print('In if')
            qs = qs.filter(vendor__startswith=self.q)
        print('Out')
        print(qs)
        return qs


class FoodVendorCreateView(CreateView):
    model = FoodVendor
    fields = ('vendor',)
    template_name = 'pool/foodvendor_form.html'
    success_url = reverse_lazy('foodvendor_list')


class FoodVendorUpdateView(UpdateView):
    model = FoodVendor
    fields = ('vendor',)
    template_name = 'pool/foodvendor_form.html'
    success_url = reverse_lazy('foodvendor_list')
