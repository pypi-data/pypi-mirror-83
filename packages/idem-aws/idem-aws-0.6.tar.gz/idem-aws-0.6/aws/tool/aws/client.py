from typing import AsyncGenerator


async def get(hub, ctx, client: str) -> AsyncGenerator:
    """
    Get a boto3 client and inject the endpoint url
    The result is an async generator so that aioboto3 keeps it's aiohttp session open
    """
    service = ctx.acct.session.client(client, endpoint_url=ctx.acct.endpoint_url)
    if hasattr(service, "__aenter__"):
        async with service as s:
            yield s
    else:
        yield service


async def request(hub, ctx, client: str, func: str, **kwargs):
    """
    Make the request for the aws resource.
    Some backends are async and some are not, work them all out here
    """
    # __aexit__ on the underlying object will be called when it's context
    # disappears at the end of this single item for loop
    async for service in hub.tool.aws.client.get(ctx, client):
        return await hub.tool.aws.wrap.awaitable(getattr(service, func), **kwargs)
