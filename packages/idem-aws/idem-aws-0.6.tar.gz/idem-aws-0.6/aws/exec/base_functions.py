from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="TODO_CLIENT",
        func="TODO_CREATE_FUNC",
        name=name,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    await hub.exec.aws.TODO_CLIENT.TODO_SUB.tag(
        ctx, name, tags={ctx.acct.provider_tag_key: name}
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="TODO_CLIENT",
        func="TODO_DELETE_FUNC",
        name=name,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="TODO_CLIENT",
        func="TODO_GET_FUNC",
        name=name,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    # Alternate method
    status, ret = await hub.aws.TODO_CLIENT.TODO_SUB.list()
    return status, ret.get(name)


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    ret = []
    status, TODO_SUBs = await hub.tool.aws.client.request(
        ctx,
        client="TODO_CLIENT",
        func="TODO_LIST_FUNC",
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    if not status:
        return status, TODO_SUBs

    for TODO_SUB in TODO_SUBs.get("TODO_ITEM_NAME", []):
        _, TODO_SUB.tags = await hub.exec.aws.TODO_CLIENT.TODO_SUB.tags(
            ctx, name=TODO_SUB.name
        )
        ret.append(TODO_SUB)
    return status, hub.tool.aws.dict.flatten_tags({"TODO_ITEMS": ret})


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="TODO_CLIENT",
        func="TODO_TAG_FUNC",
        name=name,
        dry_run=ctx.get("test", False),
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="TODO_CLIENT",
        func="TODO_GET_TAGS_FUNC",
        name=name,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    return await hub.tool.aws.client.request(
        ctx,
        client="TODO_CLIENT",
        func="TODO_UNTAG_FUNC",
        name=name,
        dry_run=ctx.get("test", False),
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx,
        client="TODO_CLIENT",
        func="TODO_UPDATE_FUNC",
        name=name,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
