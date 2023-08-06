"""
EC2 network ACL
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    return await hub.tool.aws.client.request(
        ctx, client="ec2", func="describe_network_acls", dry_run=ctx.get("test", False)
    )


async def create(hub, ctx, name: str, vpc: str, **kwargs):
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, vpc)
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_network_acl",
        dry_run=ctx.get("test", False),
        vpc_id=vpc.vpc_id,
        **kwargs,
    )
    if not status:
        return status, ret

    await hub.exec.aws.ec2.tag.create(
        ctx,
        resource_id=ret.network_acl.network_acl_id,
        tags={ctx.acct.provider_tag_key: name},
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs):
    _, network_acl = await hub.exec.aws.ec2.network_acl.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_network_acl",
        network_acl_id=network_acl.network_acl_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str):
    status, network_acls = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_network_acls",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )

    if not status or not len(network_acls.network_acls):
        return False, {}

    network_acl = network_acls.network_acls[0]
    network_acl.name = name
    return True, network_acl


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, network_acl = await hub.exec.aws.ec2.network_acl.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=network_acl.network_acl_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs):
    _, network_acl = await hub.exec.aws.ec2.network_acl.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx,
        resource_id=network_acl.network_acl_id,
        resource_type="network-acl",
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, network_acl = await hub.exec.aws.ec2.network_acl.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=network_acl.network_acl_id,
        keys=keys,
        resource_type="network-acl",
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The network_acl name
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - create_entry
            - create_tags
            - delete_entry
            - replace_association
            - replace_entry
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, network_acl = await hub.exec.aws.ec2.network_acl.get(ctx, name)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "NetworkAcl",
        action,
        resource_id=network_acl.network_acl_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
