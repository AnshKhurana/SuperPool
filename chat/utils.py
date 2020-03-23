from channels.db import database_sync_to_async

from .exceptions import ClientError
from pool.models import Service


# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_service_or_error(service_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        service = Service.objects.get(pk=service_id)
    except Service.DoesNotExist:
        raise ClientError("SERVICE_INVALID")
    # Check permissions
    # if service.staff_only and not user.is_staff:
    #     raise ClientError("SERVICE_ACCESS_DENIED")
    return service
