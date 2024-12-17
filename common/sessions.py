from aiohttp import ClientSession as AIOhttpClientSession


async def get_aiohttp_client() -> AIOhttpClientSession:
    async with AIOhttpClientSession() as client:
        yield client
        await client.close()
