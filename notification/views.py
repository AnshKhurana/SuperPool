from django.shortcuts import render
from accounts.models import User
from chat.views import food_index_internal
from pool.models import Service, ServiceMember
# Create your views here.
from django.views.generic import ListView


class notification_home(ListView):
    context_object_name = 'notification'
    template_name = 'notification/show.html'

    def get_queryset(self):
        currentuser = User.objects.get(id=self.request.user.id)
        unread = currentuser.notifications.unread()
        read = currentuser.notifications.read()
        # print('unread')
        # for x in unread:
        #     print(x.id)
        # # currentuser.notifications.mark_all_as_read()
        # print(unread)
        return unread


def mark_as_read(request, notification_id):
    print("In mark_as_read")
    currentuser = User.objects.get(id=request.user.id)
    notif_just_read = currentuser.notifications.unread().filter(id=notification_id)
    # print('notif_id')
    # print(notification_id)
    notif_just_read.mark_all_as_read()
    unread = currentuser.notifications.unread()
    return render(request, 'notification/show.html', {'notification': unread})


def mark_all_as_read(request):
    print("In mark_all_as_read")
    currentuser = User.objects.get(id=request.user.id)
    currentuser.notifications.mark_all_as_read()
    data_kwargs = food_index_internal(request)
    data_kwargs["message"] = -1
    return render(request, "chat/index.html", data_kwargs)
    # return render(request, 'chat/index.html')


def join_service(request, service_id):
    service = Service.objects.get(id=service_id)
    service_member = ServiceMember(service=service, user=request.user)
    service_member.save()
