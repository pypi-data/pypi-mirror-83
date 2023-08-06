#import os
#import requests
#
#MBTA_API_KEY = os.environ.get('MBTA_API_KEY', None)
#
#class APIKeyMissingError(Exception):
#    pass
#    
#if MBTA_API_KEY is None:
#    raise APIKeyMissingError (
#        "All methods require an API key. See "
#        "https://api-v3.mbta.com/"
#        "for how to retrieve an authentication token from "
#        "The Massachusetts Bay Transportation Authority"
#    )
#session = requests.Session()
#session.params = {}
#session.params['api_key'] = MBTA_API_KEY
#
#from .line import Line
#from .stop import Stop
#from .route import Route