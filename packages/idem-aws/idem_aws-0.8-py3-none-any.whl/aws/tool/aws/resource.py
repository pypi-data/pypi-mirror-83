from typing import AsyncGenerator, Tuple

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource: str) -> AsyncGenerator:
    """
    Get a boto3 resource and inject the endpoint url
    Handle asynchronous calls
    The result is an async generator so that aioboto3 keeps it's aiohttp session open
    """
    service = ctx.acct.session.resource(resource, endpoint_url=ctx.acct.endpoint_url)
    if hasattr(service, "__aenter__"):
        async with service as s:
            yield s
    else:
        yield service


async def request(
    hub,
    ctx,
    resource: str,
    resource_type: str,
    resource_func: str,
    resource_id: str,
    resource_args: Tuple[str] = (),
    **kwargs,
):
    """
    Make the request for the aws resource then call a funciton on it
    Some backends are async and some are not, work them all out here
    :param resource: The name of the resource to fetch (I.E. ec2)
    :param resource_type: The resource object to fetch from the resource (I.E. Vpc)
    :param resource_id: The name of the item to fetch from the object
    :param resource_func: The function to call on the named resource object
    :param resource_args: Other arguments to pass to the resource class creation
    :param kwargs: Other arguments to pass to the resource function
    """
    # __aexit__ on the underlying object will be called when it's context
    # disappears at the end of this single item for loop
    # TODO save these resources on the hub so they only get created once... but the sessions stay open until the program is over?
    async for resource in hub.tool.aws.resource.get(ctx, resource):
        resource_class = await hub.tool.aws.wrap.awaitable(
            getattr(resource, resource_type),
            resource_id,
            *resource_args,
        )

        return await hub.tool.aws.wrap.awaitable(
            getattr(resource_class, resource_func), **kwargs
        )


async def describe(
    hub,
    ctx,
    resource: str,
    resource_type: str,
    resource_id: str,
    **kwargs,
):
    """
    Describe a resource class
    :param resource: The name of the resource to fetch (I.E. ec2)
    :param resource_type: The resource object to fetch from the resource (I.E. Vpc)
    :param resource_id: The name of the item to fetch from the object
    :param resource_args: Other arguments to pass to the resource class creation
    :param kwargs: Other arguments to pass to the resource function
    """
    # __aexit__ on the underlying object will be called when it's context
    # disappears at the end of this single item for loop
    async for resource in hub.tool.aws.resource.get(ctx, resource):
        resource_class = await hub.tool.aws.wrap.awaitable(
            getattr(resource, resource_type), resource_id, **kwargs
        )
        return resource_class.meta.data
