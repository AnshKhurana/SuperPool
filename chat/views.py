from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pool.models import Service, ServiceMember, FoodService, ShoppingService, TravelService, EventService, OtherService
from django.db.models import Q

@login_required
def food_index_internal(request):
    """
    This is an internal function and should not be called via url
    """
    # Get a list of rooms, ordered alphabetically
    # services = Service.objects.order_by("title")
    # services = Service.objects.filter(members__id=request.user.id)
    services_sec = FoodService.objects.filter(
        id__in=ServiceMember.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
    # print(services_sec)
    service_prim = FoodService.objects.filter(initiator=request.user)
    # print(service_prim)
    # services = service_prim.union(services_sec)
    # print(services)

    # Render that in the index template
    return {
        "username": request.user,
        "services": service_prim,
        "other_serv": services_sec,
        "message": 2,
    }

@login_required
def food_index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    # services = Service.objects.order_by("title")
    # services = Service.objects.filter(members__id=request.user.id)
    services_sec = FoodService.objects.filter(
        id__in=ServiceMember.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
    # print(services_sec)
    service_prim = FoodService.objects.filter(initiator=request.user)
    # print(service_prim)
    # services = service_prim.union(services_sec)
    # print(services)

    # Render that in the index template
    return render(request, "chat/index.html", {
        "username": request.user,
        "services": service_prim,
        "other_serv": services_sec,
        "message": -1,
    })

@login_required
def shopping_index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    # services = Service.objects.order_by("title")
    # services = Service.objects.filter(members__id=request.user.id)
    services_sec = ShoppingService.objects.filter(
        id__in=ServiceMember.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
    # print(services_sec)
    service_prim = ShoppingService.objects.filter(initiator=request.user)
    # print(service_prim)
    # services = service_prim.union(services_sec)
    # print(services)

    # Render that in the index template
    return render(request, "chat/shopping_index.html", {
        "username": request.user,
        "services": service_prim,
        "other_serv": services_sec,
        "message": -1,
    })

@login_required
def travel_index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    # services = Service.objects.order_by("title")
    # services = Service.objects.filter(members__id=request.user.id)
    services_sec = TravelService.objects.filter(
        id__in=ServiceMember.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
    # print(services_sec)
    service_prim = TravelService.objects.filter(initiator=request.user)
    # print(service_prim)
    # services = service_prim.union(services_sec)
    # print(services)

    # Render that in the index template
    return render(request, "chat/travel_index.html", {
        "username": request.user,
        "services": service_prim,
        "other_serv": services_sec,
        "message": -1,
    })

@login_required
def event_index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    # services = Service.objects.order_by("title")
    # services = Service.objects.filter(members__id=request.user.id)
    services_sec = EventService.objects.filter(
        id__in=ServiceMember.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
    # print(services_sec)
    service_prim = EventService.objects.filter(initiator=request.user)
    # print(service_prim)
    # services = service_prim.union(services_sec)
    # print(services)

    # Render that in the index template
    return render(request, "chat/event_index.html", {
        "username": request.user,
        "services": service_prim,
        "other_serv": services_sec,
        "message": -1,
    })

@login_required
def other_index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    # services = Service.objects.order_by("title")
    # services = Service.objects.filter(members__id=request.user.id)
    services_sec = OtherService.objects.filter(
        id__in= OtherService.objects.filter(user=request.user).values('service')).exclude(initiator=request.user)
    # print(services_sec)
    service_prim = FoodService.objects.filter(initiator=request.user)
    # print(service_prim)
    # services = service_prim.union(services_sec)
    # print(services)

    # Render that in the index template
    return render(request, "chat/other_index.html", {
        "username": request.user,
        "services": service_prim,
        "other_serv": services_sec,
        "message": -1,
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
