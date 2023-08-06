"""
EC2 Placement Group
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_placement_group",
        dry_run=ctx.get("test", False),
        group_name=name,
        **kwargs,
    )
    if not status:
        return status, ret

    await hub.exec.aws.ec2.tag.create(
        ctx,
        resource_id=ret.placement_group.placement_group_id,
        tags={ctx.acct.provider_tag_key: name},
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, placement_group = await hub.exec.aws.ec2.placement_group.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_placement_group",
        placement_group_id=placement_group.placement_group_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, placement_groups = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_placement_groups",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
        **kwargs,
    )

    if not status or not len(placement_groups.placement_groups):
        return False, {}

    placement_group = placement_groups.placement_groups[0]
    placement_group.name = name
    return True, placement_group


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_placement_groups",
        dry_run=ctx.get("test", False),
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}],
        **kwargs,
    )


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, placement_group = await hub.exec.aws.ec2.placement_group.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=placement_group.placement_group_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, placement_group = await hub.exec.aws.ec2.placement_group.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx,
        resource_id=placement_group.placement_group_id,
        resource_type="placement-group",
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, placement_group = await hub.exec.aws.ec2.placement_group.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=placement_group.placement_group_id,
        keys=keys,
        resource_type="placement-group",
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, vpc: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The placement_group name
    :param vpc: The name of a vpc to attach or detach
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - attach_to_vpc
            - detach_from_vpc
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, placement_group = await hub.exec.aws.ec2.placement_group.get(ctx, name)
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, vpc)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "PlacementGroup",
        action,
        resource_id=placement_group.placement_group_id,
        vpc_id=vpc.vpc_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
