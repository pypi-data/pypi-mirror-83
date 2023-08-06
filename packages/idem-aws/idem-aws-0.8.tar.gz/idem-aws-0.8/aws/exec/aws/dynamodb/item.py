from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    table: str,
    data: Dict[str, str] = None,
    **kwargs,
):
    if data is None:
        data = {}
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="put_item",
        item={name: data},
        table_name=table,
        **kwargs,
    )


async def delete(
    hub, ctx, name: str, table: str, data: Dict[str, str] = None, **kwargs
):
    if data is None:
        data = {}

    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="delete_item",
        table_name=table,
        key={name: data},
        **kwargs,
    )


async def get(hub, ctx, name: str, table: str, **kwargs):
    status, items = await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="scan",
        table_name=table,
        attributes_to_get=[name],
        **kwargs,
    )
    if not status or not items.get("items"):
        return False, items

    return status, items["items"][0][name]


async def list_(hub, ctx, table: str, **kwargs):
    ret = {}
    status, items = await hub.tool.aws.client.request(
        ctx, client="dynamodb", func="scan", table_name=table, **kwargs
    )
    if not status:
        return status, items

    for item in items.get("items", []):
        ret.update(item)

    return status, {"items": ret}


async def update(
    hub, ctx, name: str, table: str, data: Dict[str, str] = None, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    if data is None:
        data = {}
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="update_item",
        table_name=table,
        key={name: data},
        **kwargs,
    )
