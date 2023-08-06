import asyncio
import logging
import socket
import typing

import aiohttp
import orjson
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp_socks import ProxyConnector
from aiokit import AioThing
from multidict import CIMultiDict
from python_socks import parse_proxy_url
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)
from izihawa_utils.common import noneless

from .exceptions import (
    ClientError,
    ExternalServiceError,
    MethodNotAllowedError,
    NotFoundError,
    ServiceUnavailableError,
    TemporaryError,
    WrongContentTypeError,
)


class BaseClient(AioThing):
    temporary_errors = (
        TemporaryError,
    )

    def __init__(
        self, base_url,
        default_params=None,
        default_headers=None,
        timeout=None,
        ttl_dns_cache=None,
        max_retries=2,
        retry_delay=0.5,
        proxy_url=None,
    ):
        super().__init__()
        self.base_url = base_url.rstrip('/')
        self.ttl_dns_cache = ttl_dns_cache
        self.proxy_url = proxy_url
        self.session = None
        self.default_params = CIMultiDict(noneless(default_params or {}))
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.request = retry(
            retry=retry_if_exception_type(self.temporary_errors),
            stop=stop_after_attempt(max_retries),
            wait=wait_fixed(retry_delay),
            before_sleep=before_sleep_log(logging.getLogger('aiobaseclient'), logging.WARNING),
            reraise=True,
        )(self.request)

    def headers(self, **kwargs):
        return {}

    def _create_session(self):
        proxy_kwargs = {}
        if self.proxy_url:
            proxy_kwargs['proxy_type'],\
                proxy_kwargs['host'],\
                proxy_kwargs['port'],\
                proxy_kwargs['username'],\
                proxy_kwargs['password'] = parse_proxy_url(self.proxy_url)
            connector = ProxyConnector(
                ttl_dns_cache=self.ttl_dns_cache,
                verify_ssl=False,
                **proxy_kwargs,
            )
        else:
            connector = aiohttp.TCPConnector(
                ttl_dns_cache=self.ttl_dns_cache,
                verify_ssl=False,
            )
        return aiohttp.ClientSession(connector=connector)

    async def pre_request_hook(self):
        pass

    async def request(
        self,
        method: str = 'get',
        url: str = '',
        response_processor=None,
        params=None,
        headers=None,
        json=None,
        data=None,
        timeout=None,
        *args,
        **kwargs,
    ):
        if self.session is None:
            raise RuntimeError('Client should be started before use')
        if response_processor is None:
            response_processor = self.response_processor
        all_params = CIMultiDict(self.default_params)
        all_headers = dict(self.default_headers)
        if params:
            all_params.update(noneless(params))
        if headers:
            all_headers.update(headers)
        all_headers.update(self.headers(**kwargs))

        try:
            await self.pre_request_hook()
            if json:
                if data:
                    raise ValueError('data and json parameters can not be used at the same time')
                data = orjson.dumps(json)
                if 'Content-Type' not in all_headers:
                    all_headers['Content-Type'] = 'application/json'

            response = await self.session.request(
                method,
                f"{self.base_url}/{url.lstrip('/')}",
                params=params,
                headers=noneless(all_headers),
                data=data,
                timeout=timeout or self.timeout,
            )
            if response_processor:
                return await response_processor(response)
            return response
        except ClientConnectorError as e:
            if isinstance(e.os_error, socket.gaierror) and e.errno == -2:
                raise TemporaryError(url=url, nested_error=str(e))
            elif e.errno == 111:
                raise TemporaryError(url=url, nested_error=str(e))
            else:
                raise
        except (
            aiohttp.client_exceptions.ClientOSError,
            aiohttp.client_exceptions.ServerDisconnectedError,
            asyncio.TimeoutError,
        ) as e:
            await self.session.close()
            self.session = self._create_session()
            raise TemporaryError(url=url, nested_error=str(e))

    async def delete(self, url: str = '', *args, **kwargs):
        return await self.request('delete', url, *args, **kwargs)

    async def get(self, url: str = '', *args, **kwargs):
        return await self.request('get', url, *args, **kwargs)

    async def post(self, url: str = '', *args, **kwargs):
        return await self.request('post', url, *args, **kwargs)

    async def put(self, url: str = '', *args, **kwargs):
        return await self.request('put', url, *args, **kwargs)

    async def start(self, *args, **kwargs):
        self.session = self._create_session()

    async def stop(self):
        await self.session.close()

    async def response_processor(self, response):
        text = await response.text()
        if response.status != 200:
            raise ExternalServiceError(response.request.url, response.status, text)
        return text

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()


class BaseStandardClient(BaseClient):
    def __init__(
        self, base_url,
        default_params=None,
        default_headers=None,
        timeout=None,
        ttl_dns_cache=None,
        max_retries=2,
        retry_delay=0.5,
        proxy_url=None,
    ):
        super().__init__(
            base_url=base_url,
            default_params=default_params,
            default_headers=default_headers,
            timeout=timeout,
            ttl_dns_cache=ttl_dns_cache,
            max_retries=max_retries,
            retry_delay=retry_delay,
            proxy_url=proxy_url,
        )
        self.user_token = None
        self.service_token = None

    def headers(self, with_user_token=True, with_service_token=True, cache_bypass=True, user_ip=None, **kwargs):
        return {
            **super().headers(**kwargs),
            'X-User-Token': self.user_token if with_user_token else None,
            'X-Service-Token': self.service_token if with_service_token else None,
            'X-Bypass-Cache': '1' if cache_bypass else '0',
            'X-Forwarded-For': user_ip
        }

    async def response_processor(self, response):
        data = await response.read()
        content_type = response.headers.get('Content-Type', '').lower()
        if response.status == 502 or response.status == 503:
            raise ServiceUnavailableError(status=response.status, data=data)
        elif response.status == 404:
            raise NotFoundError(status=response.status, data=data, url=response.url)
        elif response.status == 405:
            raise MethodNotAllowedError(status=response.status, url=response.url)
        else:
            if content_type.startswith('application/json'):
                try:
                    data = orjson.loads(data)
                    if isinstance(data, typing.Dict) and data.get('status') == 'error':
                        raise ClientError(**data)
                    return data
                except ValueError:
                    if response.status == 200:
                        return {}
                    raise ClientError(status=response.status, data=data)
            elif content_type.startswith('application/protobuf'):
                return data
            else:
                raise WrongContentTypeError(content_type=content_type, status=response.status, data=data)

    async def ping(self, **kwargs):
        return await self.get('/ping/', response_processor=False, **kwargs)
