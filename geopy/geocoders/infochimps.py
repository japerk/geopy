from urllib import urlencode
from urllib2 import urlopen
from geopy.geocoders.base import Geocoder

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

class Infochimps(Geocoder):
	
	BASE_URL = 'http://api.infochimps.com/geo/utils/geolocate?%s'
	
	def __init__(self, api_key, *args, **kwargs):
		super(Infochimps, self).__init__(*args, **kwargs)
		self.api_key = api_key
	
	def geocode(self, string, exactly_one=True):
		params = {
			'apikey': self.api_key,
			'f.address_text': string
		}
		
		url = self.BASE_URL % urlencode(params)
		doc = json.load(urlopen(url))
		return self.parse_json(doc, exactly_one)
	
	def parse_json(self, doc, exactly_one):
		results = doc.get('results', [])
		
		if not results:
			raise ValueError('no results found')
		
		if exactly_one:
			return self.parse_result(results[0])
		else:
			return [self.parse_result(r) for r in results]
	
	def parse_result(self, result):
		loc = '{street_number} {street_name}, {address_locality}, {state_id}, {country_id}'.format(**result)
		lng, lat = result['coordinates']
		return loc, (lat, lng)
