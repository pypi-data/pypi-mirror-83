#!/usr/local/bin/python3

from aiohttp import ( ClientSession, TCPConnector)
from aiohttp.client_exceptions import ContentTypeError
from ssl import create_default_context


# allows us to customize the session with cert files
def custom_session(path_to_cert=None, custom_headers=None):
    if path_to_cert:
        try:
            # with open | no need for importing `os` to do path.exists
            with open(path_to_cert) as cert:
                cert.read()
            sslcontext = create_default_context(cafile=path_to_cert)
            conn = TCPConnector(ssl_context=sslcontext)
        except:
            return 'Cert file not Found!'
    else:
        conn = TCPConnector(verify_ssl=False)
    session = ClientSession(connector=conn, headers=custom_headers)
    return session


class Requests:
    """
        Use `aiohttp` and `asyncio` to request data from API's

        @param `proxy`: use proxy in session if passed
    """

    def __init__(self, ca_cert=None, proxy='', headers=None):
        self.proxy = proxy
        self.cert = ca_cert
        self.headers = headers

    # takes in a request obj to extract the response | text or json
    @staticmethod
    async def get_response_from_request(request=None):
        if request is not None:
            try:
                # https://docs.aiohttp.org/en/stable/client_advanced.html#disabling-content-type-validation-for-json-responses
                # resp = await request.json(content_type='text/html; charset=utf-8')
                resp = await request.json()
            # ValueError thrown if no JSON decoded
            except ContentTypeError:
                resp = request.text
            return resp
        raise Exception('No request object passed!')

    async def do_delete(self, url):
        async with custom_session(path_to_cert=self.cert, custom_headers=self.headers) as self.session:
            async with self.session.delete(url, proxy=self.proxy) as response:
                j_resp = await self.get_response_from_request(request=response)
                return j_resp

    async def do_get(self, url, data=None):
        async with custom_session(path_to_cert=self.cert, custom_headers=self.headers) as self.session:
            async with self.session.get(url, proxy=self.proxy, params=data) as response:
                j_resp = await self.get_response_from_request(request=response)
                return j_resp

    async def do_patch(self, url, data=None):
        async with custom_session(path_to_cert=self.cert, custom_headers=self.headers) as self.session:
            async with self.session.patch(url, proxy=self.proxy, json=data) as response:
                j_resp = await self.get_response_from_request(request=response)
                return j_resp

    async def do_post(self, url, data=None):
        async with custom_session(path_to_cert=self.cert, custom_headers=self.headers) as self.session:
            async with self.session.post(url, proxy=self.proxy, json=data) as response:
                j_resp = await self.get_response_from_request(request=response)
                return j_resp

    async def do_put(self, url, data=None):
        async with custom_session(path_to_cert=self.cert, custom_headers=self.headers) as self.session:
            async with self.session.put(url, proxy=self.proxy, json=data) as response:
                j_resp = await self.get_response_from_request(request=response)
                return j_resp