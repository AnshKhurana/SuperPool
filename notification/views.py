from django.shortcuts import render
from accounts.models import User
from pool.models import Service, ServiceMember
# Create your views here.
from django.views.generic import ListView


class notification_home(ListView):
    print('Hello@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    context_object_name = 'notification'
    template_name = 'notification/show.html'

    def get_queryset(self):
        currentuser = User.objects.get(id=self.request.user.id)
        unread = currentuser.notifications.unread()
        read = currentuser.notifications.read()
        print('unread')
        print(unread)
        # currentuser.notifications.mark_all_as_read()
        print(unread)
        return unread


def mark_as_read(request, notification_id):
    currentuser = User.objects.get(id=request.user.id)
    notif_just_read = currentuser.notifications.objects.get(id=notification_id)
    notif_just_read.mark_all_as_read()
    return render(request, 'show.html')


def mark_all_as_read(request):
    currentuser = User.objects.get(id=request.user.id)
    currentuser.notifications.mark_all_as_read()
    return render(request, 'show.html')


def join_service(request, service_id):
    service = Service.objects.get(id=service_id)
    service_member = ServiceMember(service=service, user=request.user)
    service_member.save()
