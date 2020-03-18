from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from pool.models import *


class grouphome(ListView):
    # model = GroupMember
    context_object_name = 'groups'
    template_name = 'groups/groups.html'

    def get_queryset(self):
        # current_user_friends = self.request.user.friends.values('id')
        # sent_request = list(Friend.objects.filter(user=self.request.user).values_list('friend_id', flat=True))
        # users = User.objects.exclude(id__in=current_user_friends).exclude(id__in=sent_request).exclude(id=self.request.user.id)
        groups=self.request.user.groups.values_list()
        return groups
    
class GroupCreateView(CreateView):
    model=Group
    fields=['name','description']
    def get_initial(self):
        initial=super(GroupCreateView,self).get_initial()
        initial['admin']=self.request.user
        return initial

