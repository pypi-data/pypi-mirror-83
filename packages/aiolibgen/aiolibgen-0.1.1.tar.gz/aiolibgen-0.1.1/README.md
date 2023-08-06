# aiocrossref

Asynchronous client for Libgen API

## Example

```python
import asyncio

from aiolibgen import Client

async def books(base_url, ids):
    client = Client(base_url)
    return await client.by_ids(ids)

response = asyncio.get_event_loop().run_until_complete(books('https://gen.lib.rus.ec', [100500]))
```