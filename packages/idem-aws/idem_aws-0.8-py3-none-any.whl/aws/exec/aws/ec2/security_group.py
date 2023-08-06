"""
EC2 Security Group
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, description: str, vpc: str = None, **kwargs):
    if vpc:
        _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, vpc)
        kwargs["vpc_id"] = vpc.vpc_id
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_security_group",
        group_name=name,
        description=description,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    if not status:
        return status, ret
    await hub.exec.aws.ec2.tag.create(
        ctx,
        resource_id=ret.group_id,
        tags={ctx.acct.provider_tag_key: name},
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs):
    _, security_group = await hub.exec.aws.ec2.security_group.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_security_group",
        group_id=security_group.group_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str):
    status, security_groups = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_security_groups",
        group_names=[name],
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )

    if not status or not len(security_groups.security_groups):
        return False, {}

    security_group = security_groups.security_groups[0]
    security_group.name = name
    return True, security_group


async def list_(hub, ctx):
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_security_groups",
        dry_run=ctx.get("test", False),
    )


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, security_group = await hub.exec.aws.ec2.security_group.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=security_group.group_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs):
    status, security_group = await hub.exec.aws.ec2.security_group.get(
        ctx, name, **kwargs
    )
    return status, {"tags": security_group.tags}


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, security_group = await hub.exec.aws.ec2.security_group.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=security_group.group_id,
        keys=keys,
        resource_type="security-group",
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The security_group name
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - authorize_egress
            - authorize_ingress
            - revoke_egress
            - revoke_ingress
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, security_group = await hub.exec.aws.ec2.security_group.get(ctx, name)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "SecurityGroup",
        action,
        resource_id=security_group.group_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
