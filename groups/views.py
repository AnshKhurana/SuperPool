from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from pool.models import *
from .forms import *
from accounts.models import User


class grouphome(ListView):
    # model = GroupMember
    context_object_name = 'groups'
    template_name = 'groups/groups.html'

    def get_queryset(self):
        currentuser=User.objects.get(id=self.request.user.id)
        groups = Group.objects.filter(members=currentuser).all()
        return groups


class GroupListView(ListView):
    model = Group
    # queryset = Group.objects.filter(id=g_id)
    # form_class = GroupCreateForm
    # success_url = '/groups'

    # def get_initial(self):
    #     initial=super(GroupCreateView,self).get_initial()
    #     initial['admin_id']=self.request.user.id
    #     return initial
    # def form_valid(self, form):
    #     form.instance.admin=User.objects.get(id=self.request.user.id)
    #     return super(GroupCreateView,self).form_valid(form)

    def get_queryset(self):
        context = Group.objects.filter(id=self.kwargs['g_id'])
        print(context)
        return context



class GroupCreateView(CreateView):
    model = Group
    form_class = GroupCreateForm
    success_url = '/groups'

    # def get_initial(self):
    #     initial=super(GroupCreateView,self).get_initial()
    #     initial['admin_id']=self.request.user.id
    #     return initial
    # def form_valid(self, form):
    #     form.instance.admin=User.objects.get(id=self.request.user.id)
    #     return super(GroupCreateView,self).form_valid(form)
    
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):

        user_form = GroupCreateForm(data=request.POST)

        if user_form.is_valid():
            group = user_form.save()
            member = self.request.user
            group.members.add(member)
            group.admin=User.objects.get(id=self.request.user.id)
            group.save()
            client_ip = request.META['REMOTE_ADDR']
            join_url="http://" + client_ip + ":{}/groups/join/".format(request.META['SERVER_PORT']) + str(group.hash)
            return HttpResponse("<h>%s</h>" % join_url)
        else:
            print(user_form.errors)
            return render(request, 'accounts/register.html', {'form': user_form})


def group_join(request, hash):
    data = request.POST
    cur_user = request.user
    group = Group.objects.filter(hash=hash)[0]
    member = GroupMember(group=group, user=cur_user)
    member.save()
    return HttpResponse("<h>%s</h>" % "Added to group successfully")
