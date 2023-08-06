import asyncio
import time
from typing import (
    Dict,
    Iterable,
)

import orjson as json
from aiobaseclient import BaseClient

from aiolibgen.exceptions import (
    ClientError,
    ExternalServiceError,
    NotFoundError,
)


class Client(BaseClient):
    default_fields = [
        'title',
        'author',
        'md5',
        'filesize',
        'descr',
        'edition',
        'extension',
        'pages',
        'series',
        'year',
        'language',
        'identifier',
        'id',
        'coverurl',
        'doi',
        'tags',
        'timelastmodified',
    ]

    def __init__(
        self,
        base_url,
        user_agent: str = None,
        delay: float = 1.0 / 50.0,
        **kwargs
    ):
        headers = {}
        if user_agent:
            headers['User-Agent'] = user_agent
        super().__init__(base_url=base_url, default_headers=headers, **kwargs)
        self.delay = delay
        self.last_query_time = 0.0

    async def pre_request_hook(self):
        t = time.time()
        if t - self.last_query_time < self.delay:
            await asyncio.sleep(t - self.last_query_time)
        self.last_query_time = t

    async def by_ids(self, ids, fields=None):
        if not fields:
            fields = self.default_fields
        if not isinstance(ids, Iterable):
            ids = [ids]
        ids = list(map(str, ids))
        r = await self.get(
            '/json.php',
            params={
                'ids': ','.join(ids),
                'fields': ','.join(fields),
            }
        )
        return r

    async def newer(self, timenewer, idnewer=0, fields=None):
        if not fields:
            fields = self.default_fields
        while True:
            rows = await self.get(
                '/json.php',
                params={
                    'fields': ','.join(fields),
                    'mode': 'newer',
                    'timenewer': timenewer,
                    'idnewer': idnewer,
                }
            )
            if not rows:
                return
            for row in rows:
                timenewer = row['timelastmodified']
                idnewer = row['id']
                yield row

    async def response_processor(self, response):
        text = await response.text()
        if response.status == 404:
            raise NotFoundError(status=response.status, text=response.text, url=response.url)
        elif response.status != 200:
            raise ExternalServiceError(response.url, response.status, text)
        data = json.loads(text)
        if isinstance(data, Dict) and 'error' in data:
            raise ClientError(**data)
        return data
