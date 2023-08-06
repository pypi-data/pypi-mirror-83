__func_alias__ = {"list_": "list"}


def __virtual__(hub):
    return False, "Until this can be tested it isn't production ready"


async def list_(hub, ctx):
    ret = {}
    status, backups = await hub.tool.aws.client.request(
        ctx, client="dynamodb", func="list_backups"
    )
    if not status:
        return status, backups
    for backup in backups.get("backup_summaries", []):
        _, ret[backup["backup_name"]] = backup
    return status, ret


async def get(hub, ctx, backup_arn: str):
    status, ret = await hub.tool.aws.client.request(
        ctx, client="dynamodb", func="describe_backup", backup_arn=backup_arn
    )
    ret = ret.get("table", {})
    if ret:
        _, tags = await hub.tool.aws.client.request(
            ctx,
            client="dynamodb",
            func="list_tags_of_resource",
            resource_arn=ret["backup_arn"],
        )
        ret["tags"] = tags.get("tags", {})
    return status, ret


async def create(
    hub,
    ctx,
    name: str,
    table: str,
):
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="create_backup",
        backup_name=name,
        table_name=table,
    )


async def delete(
    hub,
    ctx,
    name: str,
):
    return await hub.tool.aws.client.request(
        ctx,
        client="dynamodb",
        func="delete_backup",
        table_name=name,
    )
