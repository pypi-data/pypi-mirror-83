"""
EC2 Route
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, vpc: str, **kwargs):
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, vpc)
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_route_table",
        vpc_id=vpc.vpc_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    if not status:
        return status, ret
    await hub.exec.aws.ec2.tag.create(
        ctx,
        resource_id=ret.route_table.route_table_id,
        tags={ctx.acct.provider_tag_key: name},
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs):
    _, route_table = await hub.exec.aws.ec2.route_table.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_route_table",
        route_table_id=route_table.route_table_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str):
    status, route_tables = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_route_tables",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )

    if not status or not len(route_tables.route_tables):
        return False, {}

    route_table = route_tables.route_tables[0]
    route_table.name = name
    return True, route_table


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, route_table = await hub.exec.aws.ec2.route_table.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=route_table.route_table_id, tags=tags, **kwargs
    )


async def list_(hub, ctx):
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_route_tables",
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}],
        dry_run=ctx.get("test", False),
    )


async def tags(hub, ctx, name: str, **kwargs):
    _, route_table = await hub.exec.aws.ec2.route_table.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx,
        resource_id=route_table.route_table_id,
        resource_type="route-table",
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, route_table = await hub.exec.aws.ec2.route_table.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=route_table.route_table_id,
        keys=keys,
        resource_type="route-table",
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The route_table name
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - associate_with subnet
            - create_route

    :param kwargs: keyword arguments to pass to the resource action
    """
    _, route_table = await hub.exec.aws.ec2.route_table.get(ctx, name)
    status, result = await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "RouteTable",
        action,
        resource_id=route_table.route_table_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    return status is not False, result.meta.data
