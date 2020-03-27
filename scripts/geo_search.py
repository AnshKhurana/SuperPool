import requests
import json
api_key = 'J6updMEyBoTKrXSBqhOpjO1sP64AjPPB2FwKPwJUNfU'
# raw_query='''https: // autocomplete.geocoder.ls.hereapi.com/6.2/suggest.json?apiKey = {{{}}}&query=Pariser+1+Berl&beginHighlight = <b >&endHighlight = </b >'''.format(api_key).replace(' ','')
raw_query = '''https://autocomplete.geocoder.ls.hereapi.com/6.2/suggest.json'''
print('DO NOT QUERY TOO MUCH !!!')
print(raw_query)
response=requests.get(raw_query,params={
    'apiKey': api_key,
    'query':input('Enter Search Text: ')
}).json()



print(json.dumps(response,indent=2))


