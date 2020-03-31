import json

import requests

company_api_url = "https://autocomplete.clearbit.com/v1/companies/suggest"
response = requests.get(company_api_url, params={'query': input("Enter company name: ")}).json()
print(json.dumps(response, indent=2))
