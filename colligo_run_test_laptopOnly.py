from colligo.base.types.tensor import Tensor
from colligo.base.worker_registery import set_worker_registery
from colligo.sdk import HttpClient

from colligo.models.firefly.clio_v2.types import CLIO_V2, ClioExecutor, ClioRequest

async def test():
    set_worker_registery(HttpClient("https://text2image-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net"))
    request = ClioRequest(gi_PROMPT="A man in black suite", gi_SEED=[132434, 234])

    response = await ClioExecutor.call(request)

    print(response)


import asyncio

async def main():
    await test()

asyncio.run(main())
