""" Base script used across defined """

import requests
import vesicashapi as api

class Borg:
    """ Borg class making class attributes global """
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

class VesicashBase(Borg):
    """Base Class used across defined."""

    def __init__(self, **kwargs):
        """ Initialize Vesicash with private key"""
        Borg.__init__(self)
        private_key = kwargs.get('private_key', api.PRIVATE_KEY)
        authorization = api.HEADERS['V-Private-Key']

        headers = {'V-Private-Key': private_key}

        arguments = dict(api_url=api.API_URL, headers=headers)
        if not hasattr(self, 'requests'):
            req = VesicashRequests(**arguments)
            self._shared_state.update(requests=req)

class VesicashRequests(object):

    def __init__(self, api_url = 'https://sandbox.api.vesicash.com/v1/', headers=None):
        """Initialize Vesicash Request object for browsing resource.
		Args:
			api_url: str
			headers: dict
		"""
        self.API_BASE_URL = f"{api_url}"
        self.headers = headers

    def _request(self, method, resource_uri, **kwargs):
        """Perform a method on a resource.
		Args:
			method: requests.`method`
			resource_uri: resource endpoint
		Raises:
			HTTPError
		Returns:
			JSON Response
		"""
        data = kwargs.get('data')
        qs = kwargs.get('qs')
        response = method(
			self.API_BASE_URL + resource_uri,
			json=data, headers=self.headers,
			params=qs
		)
        return response.json() if response.status_code != 401 else response.text

    def get(self, endpoint, **kwargs):
        """Get a resource.
		Args:
			endpoint: resource endpoint.
		"""
        return self._request(requests.get, endpoint, **kwargs)
        
    def post(self, endpoint, **kwargs):
        """Create a resource.
		Args:
			endpoint: resource endpoint.
		"""
        return self._request(requests.post, endpoint, **kwargs)
        
    def put(self, endpoint, **kwargs):
        """Update a resource.
		Args:
			endpoint: resource endpoint.
		"""
        return self._request(requests.put, endpoint, **kwargs)
