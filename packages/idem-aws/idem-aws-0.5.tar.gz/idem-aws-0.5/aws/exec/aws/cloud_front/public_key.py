from typing import Any, Dict, List, Tuple
from datetime import datetime

__func_alias__ = {"list_": "list"}


async def create(
    hub, ctx, name: str, encoded_key: str, comment: str = None
) -> Tuple[bool, Dict[str, Any]]:
    public_key_config = {
        "Name": name,
        "CallerReference": str(datetime.now().timestamp()).replace(".", ""),
        "EncodedKey": encoded_key,
    }
    if comment:
        public_key_config["Comment"] = comment
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="create_public_key",
        public_key_config=public_key_config,
    )
    await hub.exec.aws.cloud_front.public_key.tag(
        ctx, name, tags={ctx.acct.provider_tag_key: name}
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, foo = await hub.exec.aws.cloud_front.public_key.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="delete_public_key",
        name=name,
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="get_public_key",
        name=name,
        **kwargs,
    )
    # Alternate method
    status, ret = await hub.aws.cloud_front.public_key.list()
    return status, ret.get(name)


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    ret = []
    status, public_keys = await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="list_public_keys",
        **kwargs,
    )
    if not status:
        return status, public_keys

    for public_key in public_keys.get("TODO_ITEM_NAME", []):
        _, public_key.tags = await hub.exec.aws.cloud_front.public_key.tags(
            ctx, name=public_key.name
        )
        ret.append(public_key)
    return status, hub.tool.aws.dict.flatten_tags({"TODO_ITEMS": ret})


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="TODO_TAG_FUNC",
        name=name,
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="TODO_GET_TAGS_FUNC",
        name=name,
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="TODO_UNTAG_FUNC",
        name=name,
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="TODO_UPDATE_FUNC",
        name=name,
        **kwargs,
    )
