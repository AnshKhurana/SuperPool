from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pool.models import Service, ServiceMember, FoodService
from django.db.models import Q


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    # services = Service.objects.order_by("title")
    # services = Service.objects.filter(members__id=request.user.id)
    services_sec = Service.objects.filter(
        id__in=ServiceMember.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
    # print(services_sec)
    service_prim = Service.objects.filter(initiator=request.user)
    # print(service_prim)
    # services = service_prim.union(services_sec)
    # print(services)

    # Render that in the index template
    return render(request, "chat/index.html", {
        "username": request.user,
        "services": service_prim,
        "other_serv": services_sec,
    })


def after_disable(request, service_id):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    # services = Service.objects.order_by("title")
    # services = Service.objects.filter(members__id=request.user.id)
    s_as_qset = Service.objects.filter(id=service_id)
    s_as_obj = Service.objects.get(id=service_id)
    print("is_active field of current service = " + str(s_as_obj.is_active))

    if request.user != s_as_obj.initiator:
        print('Internal error at chat/views line 40')
    if s_as_obj.is_active:
        s_as_qset.update(is_active=False)
    else:
        s_as_qset.update(is_active=True)

    services_sec = Service.objects.filter(
        id__in=ServiceMember.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
    # print(services_sec)
    service_prim = Service.objects.filter(initiator=request.user)
    # print(service_prim)
    # services = service_prim.union(services_sec)
    # print(services)

    # Render that in the index template
    print('redirecting')
    return redirect('../', {
        "username": request.user,
        "services": service_prim,
        "other_serv": services_sec,
    })
