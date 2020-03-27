from django.shortcuts import render
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
    services_sec = Service.objects.filter(id__in=ServiceMember.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
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
