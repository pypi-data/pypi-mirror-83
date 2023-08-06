from .auth import Auth
from .const import *

class MBTA:
    def __init__(self, auth):
        self.auth = auth
        
    async def getStop(self, id, payload=None):
        """Get the details for a stop."""
        response = await self.auth.request(
            "get", f'{ENDPOINT_STOPS}/{id}', payload)
        return await response.json()
        
    async def getTrip(self, id, payload=None):
        """Get the details for a trip."""
        response = await self.auth.request(
            "get", f'{ENDPOINT_TRIPS}/{id}', payload)
        return await response.json()
        
    async def getRoute(self, id, payload=None):
        """Get the details for a route."""
        response = await self.auth.request(
            "get", f'{ENDPOINT_ROUTES}/{id}', payload)
        return await response.json()
        
    async def listPredictions(self, payload):
        """Get a list of Predictions."""
        response = await self.auth.request(
            "get", f'{ENDPOINT_PREDICTIONS}', params=payload
        )
        return await response.json()
        
    async def listStops(self, payload=None):
        """Get a list of Stops."""
        response = await self.auth.request(
            "get", f'{ENDPOINT_STOPS}', params=payload
        )
        return await response.json()