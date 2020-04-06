import requests

url = "https://us1.locationiq.com/v1/autocomplete.php"
KEY = 'c635736cc00334'
COUNTRY_CODE = 'in'
LIMIT = 15

while 1:
    loc = input()
    data = {
        'key': KEY,
        'q': loc,
        'countrycodes': COUNTRY_CODE,
        'limit': LIMIT,
        'format': 'json'
    }

    response_obj = requests.get(url, params=data)

    response_json = response_obj.json()

    for i, loc_json in enumerate(response_json):
        print(i + 1, loc_json['display_name'], sep=' ')
