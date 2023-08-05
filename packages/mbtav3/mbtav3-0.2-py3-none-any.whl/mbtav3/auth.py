from aiohttp import ClientConnectorError, ClientResponse, ClientSession
import os

MBTA_DEFAULT_HOST = "api-v3.mbta.com"

class Auth:
    """Class to make authenticated requests to the MBTA v3 API."""
    
    def __init__(
        self,
        websession: ClientSession,
        api_key: str = None,
        host: str = MBTA_DEFAULT_HOST,
        
    ):
        """Initialize the auth."""
        self.websession = websession
        self.api_key = api_key
        self.host = host
        
        if api_key == None:
            self.api_key = os.environ.get('MBTA_API_KEY')
        
    async def request(
        self, method: str, path: str, payload=None, **kwargs
    ) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")
        
        if headers is None:
            headers = {}
        else:
            headers = dict(headers)
            
        headers['api_key'] = self.api_key
        
        try:
            response = await self.websession.request(
                method,
                f'https://{self.host}/{path}',
                json=payload,
                **kwargs,
                headers=headers,
            )
            
            data = await response.json()
            
            return_code = data.get("returnCode")
            
            return response
            
        except ClientConnectorError as error:
            raise CannotConnect(error)