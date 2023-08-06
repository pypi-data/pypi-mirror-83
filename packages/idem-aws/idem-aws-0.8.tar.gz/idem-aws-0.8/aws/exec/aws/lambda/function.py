from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    runtime: str,
    role: str,
    handler: str,
    code: Dict[str, str],
    tags: Dict[str, str] = None,
    **kwargs,
):
    status, role = await hub.exec.aws.iam.role.get(ctx, role)
    if not status:
        return status, role

    if tags is None:
        tags = {}

    tags[ctx.acct.provider_tag_key] = name
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="create_function",
        function_name=name,
        runtime=runtime,
        role=role.arn,
        handler=handler,
        code=code,
        tags=tags,
        **kwargs,
    )


async def delete(hub, ctx, name: str):
    return await hub.tool.aws.client.request(
        ctx, client="lambda", func="delete_function", function_name=name
    )


async def get(hub, ctx, name: str, **kwargs):
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="get_function",
        function_name=name,
        **kwargs,
    )
    ret.name = name

    return status, ret


async def list_(hub, ctx, **kwargs):
    ret = []
    status, functions = await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="list_functions",
        **kwargs,
    )
    if not status:
        return status, functions
    for func in functions.get("functions", []):
        name = func.function_name
        _, item = await hub.exec.aws.λ.function.get(ctx, name)
        ret.append(item)

    return status, {"functions": ret}


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, func = await hub.exec.aws.λ.function.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="tag_resource",
        resource=func.configuration.function_arn,
        tags=tags,
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, func = await hub.exec.aws.λ.function.get(ctx, name, **kwargs)
    return status, {"tags": func.get("tags", {})}


async def untag(hub, ctx, name: str, keys: List[str], **kwargs):
    _, func = await hub.exec.aws.λ.function.get(ctx, name, **kwargs)
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="untag_resource",
        resource=func.configuration.function_arn,
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, update_function: str, name: str, **kwargs):
    """
    :param name: The name of the function to update
    :param update_function:  one of "code", "configuration", or "event_invoke_config"
    """
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func=f"update_function_{update_function}",
        function_name=name,
        **kwargs,
    )
