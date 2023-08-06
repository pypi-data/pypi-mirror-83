from typing import List

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    replication_group: List[str] = None,
):
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="create_global_table",
        global_table_name=name,
        replication_group=[
            {"RegionName": region} for region in (replication_group or [])
        ],
    )


async def delete(
    hub,
    ctx,
    name: str,
    replication_group: List[str] = None,
):
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="update_global_table",
        global_table_name=name,
        replica_updates=[
            {"Delete": {"RegionName": region} for region in (replication_group or [])}
        ],
    )


async def get(hub, ctx, name: str):
    status, ret = await hub.tool.aws.client.request(
        ctx, client="dynamodb", func="describe_global_table", global_table_name=name
    )
    ret = ret.get("global_table_description", {})
    if ret:
        resource_arn = ret.get("global_table_arn")
        if resource_arn:
            _, tags = await hub.tool.aws.client.request(
                ctx,
                client="dynamodb",
                func="list_tags_of_resource",
                resource_arn=resource_arn,
            )
            ret["tags"] = tags.get("tags", {})
    return status, ret


async def list_(hub, ctx, **kwargs):
    ret = {}
    status, tables = await hub.tool.aws.client.request(
        ctx, client="dynamodb", func="list_global_tables", **kwargs
    )
    if not status:
        return status, tables
    for table in tables.get("global_tables", []):
        name = table["global_table_name"]
        _, item = await hub.exec.aws.dynamodb.global_table.get(ctx, name)
        ret[name] = item
    return status, {"global_tables": ret}
