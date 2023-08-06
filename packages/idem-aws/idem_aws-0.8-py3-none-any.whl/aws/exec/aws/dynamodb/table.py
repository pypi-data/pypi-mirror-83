from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    attribute_definitions: List[Dict[str, str]],
    key_schema: List[str],
    tags: List[str] = None,
    **kwargs,
):
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="create_table",
        table_name=name,
        attribute_definitions=attribute_definitions,
        key_schema=key_schema,
        tags=[{"Key": ctx.acct.provider_tag_key, "Value": name}] + (tags or []),
        **kwargs,
    )


async def delete(
    hub,
    ctx,
    name: str,
):
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="delete_table",
        table_name=name,
    )


async def get(hub, ctx, name: str):
    status, ret = await hub.tool.aws.client.request(
        ctx, client="dynamodb", func="describe_table", table_name=name
    )
    ret = ret.get("table", {})
    if ret:
        _, tags = await hub.tool.aws.client.request(
            ctx,
            client="dynamodb",
            func="list_tags_of_resource",
            resource_arn=ret["table_arn"],
        )
        ret.tags = tags.get("tags", {})
        ret.name = name
    return status, ret


async def list_(hub, ctx):
    ret = []
    status, tables = await hub.tool.aws.client.request(
        ctx, client="dynamodb", func="list_tables"
    )
    if not status:
        return status, tables
    for table in tables.get("table_names", []):
        _, item = await hub.exec.aws.dynamodb.table.get(ctx, table)
        ret.append(item)
    return status, {"tables": ret}


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, table = await hub.exec.aws.dynamodb.table.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="tag_resource",
        resource_arn=table.table_arn,
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, table = await hub.exec.aws.dynamodb.table.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="list_tags_of_resource",
        resource_arn=table.table_arn,
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, table = await hub.exec.aws.dynamodb.table.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="untag_resource",
        resource_arn=table.table_arn,
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx, client="dynamodb", func="update_table", table_name=name, **kwargs
    )
