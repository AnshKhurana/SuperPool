from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView

from chat.views import food_index_internal
from pool.models import *
from .forms import *
from accounts.models import User


class grouphome(ListView):
    # model = GroupMember
    context_object_name = 'groups'
    template_name = 'groups/groups.html'

    def get_queryset(self):
        currentuser = User.objects.get(id=self.request.user.id)
        groups = Group.objects.filter(members=currentuser).all()
        return groups


class GroupListView(DetailView):
    model = Group
    context_object_name = 'group'
    # template_name = 'pool/group_list.html'
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

    # def get_queryset(self):
    #     # group = Group.objects.get(id=self.kwargs['g_id'])
    #     if group.admin == self.request.user:
    #         self.template_name = 'groups/group_info_admin.html'
    #     else:
    #         self.template_name = 'groups/group_info_non_admin.html'
    #     print(group)
    #     return group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['group'].admin == self.request.user:
            self.template_name = 'groups/group_info_admin.html'
        else:
            self.template_name = 'groups/group_info_non_admin.html'
        context["g_id"] = context['group'].id
        client_ip = self.request.META['REMOTE_ADDR']
        context["join_url"] = "http://" + client_ip + ":{}/groups/join/".format(self.request.META['SERVER_PORT']) + str(context['group'].hash)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(GroupListView, self).get_context_data(**kwargs)
    #     print(context['group_list'][0])
    #     context['user'] = 0
    #     if context['group_list'][0] in Group.objects.filter(admin=self.request.user):
    #         context['user'] = 1
    #     return context


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
            group.admin = User.objects.get(id=self.request.user.id)
            group.save()
            client_ip = request.META['REMOTE_ADDR']
            join_url = "http://" + client_ip + ":{}/groups/join/".format(request.META['SERVER_PORT']) + str(group.hash)
            data_kwargs = food_index_internal(self.request)
            data_kwargs["message"] = "Group Create" + join_url
            return render(self.request, "chat/index.html", data_kwargs)
        else:
            print(user_form.errors)
            return render(request, 'accounts/register.html', {'form': user_form})


@login_required(login_url="/accounts/login/")
def group_join(request, hash):
    data = request.POST
    cur_user = request.user
    group = Group.objects.filter(hash=hash)[0]
    member = GroupMember(group=group, user=cur_user)
    member.save()
    return render(request, 'home.html', {'message': "Group Join"})


def remove_member(request, g_id, user_id):
    group = Group.objects.get(id=g_id)
    user = User.objects.get(id=user_id)
    group_member = GroupMember.objects.get(group=group, user=user)
    group_member.delete()
    data_kwargs = food_index_internal(request)
    data_kwargs["message"] = "Group Remove"
    return render(request, "chat/index.html", data_kwargs)
