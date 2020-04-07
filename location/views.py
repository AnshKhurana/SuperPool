from django.shortcuts import render
from django.conf import settings
import requests
from dal import autocomplete
from datetime import datetime
from pool.models import Location


# Create your views here.
class LocationAutocomplete(autocomplete.Select2QuerySetView):
    # model = FoodVendor
    # context_object_name = 'Food Vendor'
    # template_name = 'pool/foodvendor_form.html'

    def get_queryset(self):
        url = "https://us1.locationiq.com/v1/autocomplete.php"
        KEY = 'c635736cc00334'
        COUNTRY_CODE = 'in'
        LIMIT = 15
        current_time = datetime.now()
        if self.q:
            data = {
                'key': KEY,
                'q': self.q,
                'countrycodes': COUNTRY_CODE,
                'limit': LIMIT,
                'format': 'json'
            }
            responses = requests.get(url, params=data).json()
            for response in responses:
                print(response.keys())
                if 'error' in response.keys():
                    break
                location = Location(latitude=response['lat'],
                                    longitude=response['lon'],
                                    address=response['display_address'],
                                    timestamp=current_time)
                location.save()
        qs = Location.objects.filter(timestamp=current_time)
        print(qs)
        return qs
