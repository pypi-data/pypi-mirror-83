from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


FUNCTION_ARN = lambda alias_arn: ":".join(alias_arn.split(":")[:7])


async def list_(hub, ctx, function_name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    ret = []
    status, items = await hub.tool.aws.client.request(
        ctx, client="lambda", func="list_aliases", function_name=function_name, **kwargs
    )
    if not status:
        return status, items

    for item in items.get("aliases", []):
        _, alias = await hub.exec.aws.λ.alias.get(
            ctx, name=item.name, function_name=function_name
        )
        ret.append(alias)
    return status, {"aliases": ret}


async def create(
    hub, ctx, name: str, function_name: str, function_version: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="create_alias",
        name=name,
        function_name=function_name,
        function_version=function_version,
        **kwargs,
    )
    if not status:
        return status, ret

    await _tag(
        hub,
        ctx,
        resource_arn=FUNCTION_ARN(ret.alias_arn),
        tags={ctx.acct.provider_tag_key: name},
    )
    return status, ret


async def delete(
    hub, ctx, name: str, function_name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="delete_alias",
        name=name,
        function_name=function_name,
        **kwargs,
    )


async def _get(hub, ctx, name: str, function_name: str, **kwargs):
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="get_alias",
        name=name,
        function_name=function_name,
        **kwargs,
    )


async def get(
    hub, ctx, name: str, function_name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await _get(hub, ctx, name, function_name, **kwargs)
    if not status:
        return status, ret

    _, tags = await _tags(hub, ctx, resource_arn=FUNCTION_ARN(ret.alias_arn))
    ret.tags = tags.tags
    return status, ret


async def _tag(hub, ctx, resource_arn: str, tags: Dict[str, str], **kwargs):
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="tag_resource",
        resource=resource_arn,
        tags=tags,
        **kwargs,
    )


async def tag(
    hub, ctx, name: str, function_name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, alias = await _get(hub, ctx, name=name, function_name=function_name)
    return await _tag(
        hub, ctx, resource_arn=FUNCTION_ARN(alias.alias_arn), tags=tags, **kwargs
    )


async def _tags(hub, ctx, resource_arn: str, **kwargs):
    return await hub.tool.aws.client.request(
        ctx, client="lambda", func="list_tags", resource=resource_arn, **kwargs
    )


async def tags(
    hub, ctx, name: str, function_name, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, alias = await _get(hub, ctx, name, function_name)
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="list_tags",
        resource=FUNCTION_ARN(alias.alias_arn),
        **kwargs,
    )


async def untag(hub, ctx, name: str, function_name, keys: List[str], **kwargs):
    _, alias = await _get(hub, ctx, name, function_name)
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="untag_resource",
        resource=FUNCTION_ARN(alias.alias_arn),
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, function_name: str, **kwargs):
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx,
        client="lambda",
        func="update_alias",
        name=name,
        function_name=function_name,
        **kwargs,
    )
