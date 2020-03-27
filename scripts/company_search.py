import json
import sys

import requests

company_api_url = "https://autocomplete.clearbit.com/v1/companies/suggest"
query_string = sys.argv[1]
response = requests.get(company_api_url, params={'query': query_string}).json()
for x in response:
    print(x['name'])
# print(json.dumps(response, indent=2))
