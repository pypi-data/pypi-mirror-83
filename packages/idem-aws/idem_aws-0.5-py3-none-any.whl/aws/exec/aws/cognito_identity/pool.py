# Cognito identity pool
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    allow_unauthenticated_identities: bool,
    tags: Dict[str, Any] = None,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    if tags is None:
        tags = {}
    tags[ctx.acct.provider_tag_key] = name
    return await hub.tool.aws.client.request(
        ctx,
        client="cognito-identity",
        func="create_identity_pool",
        identity_pool_name=name,
        identity_pool_tags=tags,
        allow_unauthenticated_identities=allow_unauthenticated_identities,
        **kwargs,
    )


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cognito-identity",
        func="delete_identity",
        name=name,
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await hub.exec.aws.cognito_identity.pool.list(ctx, **kwargs)
    return status and name in ret, ret.get(name, {})


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    ret = []
    status, pools = await hub.tool.aws.client.request(
        ctx,
        client="cognito-identity",
        func="list_identity_pools",
        max_results=500,
        **kwargs,
    )
    if not status:
        return status, pools

    for pool in pools.get("identity_pools", []):
        _, p = await hub.tool.aws.client.request(
            ctx,
            client="cognito-identity",
            func="describe_identity_pool",
            identity_pool_id=pool.identity_pool_id,
            **kwargs,
        )
        p.tags = p.pop("identity_pool_tags")
        p.name = pool.identity_pool_name
        ret.append(p)
    return status, hub.tool.aws.dict.flatten_tags({"TODO_ITEMS": ret})


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cognito-identity",
        func="TODO_TAG_FUNC",
        name=name,
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cognito-identity",
        func="list_tags_for_resource",
        name=name,
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cognito-identity",
        func="TODO_UNTAG_FUNC",
        name=name,
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx,
        client="cognito-identity",
        func="TODO_UPDATE_FUNC",
        name=name,
        **kwargs,
    )
