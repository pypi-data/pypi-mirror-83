from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="kms",
        func="create_key",
        tags=[{"TagKey": ctx.acct.provider_tag_key, "TagValue": name}],
        **kwargs,
    )

    return status, ret


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, key = await hub.exec.aws.kms.key.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="kms",
        func="disable_key",
        key_id=key.key_id,
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, keys = await hub.exec.aws.kms.key.list(ctx, **kwargs)
    return status and name in keys, keys.get(name, {})


async def list_(
    hub, ctx, max_count: int = 100, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, keys = await hub.tool.aws.client.request(
        ctx,
        client="kms",
        func="list_keys",
        limit=max_count,
        **kwargs,
    )
    if not status:
        return status, keys

    ret = {}
    for key in keys.get("keys", []):
        _, t = await _tags(hub, ctx, key_id=key.key_id)
        key.tags = t.get("tags", {})
        name = key.tags.get(ctx.acct.provider_tag_key)
        if not name:
            continue
        key.name = name
        ret[name] = key
    return status, {"keys": ret}


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, key = await hub.exec.aws.kms.key.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="kms",
        func="tag_resource",
        key_id=key.key_id,
        tags=[{"TagKey": k, "TagValue": v} for k, v in tags.items()],
        **kwargs,
    )


async def _tags(hub, ctx, key_id: str, max_count: int = 50, **kwargs):
    return await hub.tool.aws.client.request(
        ctx,
        client="kms",
        func="list_resource_tags",
        key_id=key_id,
        limit=max_count,
        **kwargs,
    )


async def tags(
    hub, ctx, name: str, max_count: int = 50, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, key = await hub.exec.aws.kms.key.get(ctx, name)
    return await _tags(hub, ctx, key_id=key.key_id, max_count=max_count)


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, key = await hub.exec.aws.kms.key.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="kms",
        func="untag_resource",
        key_id=key.key_id,
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, key = await hub.exec.aws.kms.key.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="kms",
        func="update_key_description",
        key_id=key.key_id,
        **kwargs,
    )
