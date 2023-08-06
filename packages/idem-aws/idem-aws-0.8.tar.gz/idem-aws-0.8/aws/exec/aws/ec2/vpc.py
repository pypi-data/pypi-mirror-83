"""
EC2 VPC
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, cidr_block: str, **kwargs):
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_vpc",
        cidr_block=cidr_block,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    if not status:
        return status, ret
    await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=ret.vpc.vpc_id, tags={ctx.acct.provider_tag_key: name}
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs):
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_vpc",
        vpc_id=vpc.vpc_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str):
    status, vpcs = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_vpcs",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )

    if not status or not len(vpcs.vpcs):
        return False, {}

    vpc = vpcs.vpcs[0]
    vpc.name = name
    return True, vpc


async def list_(hub, ctx):
    return await hub.tool.aws.client.request(
        ctx, client="ec2", func="describe_vpcs", dry_run=ctx.get("test", False)
    )


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=vpc.vpc_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs):
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx, resource_id=vpc.vpc_id, resource_type="vpc", **kwargs
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx, resource_id=vpc.vpc_id, keys=keys, resource_type="vpc", **kwargs
    )


async def update(
    hub, ctx, action: str, name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The vpc name
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - associate_dhcp_options
            - attach_classic_link_instance
            - attach_internet_gateway
            - create_network_acl
            - create_route_table
            - create_security_group
            - create_subnet
            - describe_attribute
            - detach_classic_link_instance
            - detach_internet_gateway
            - disable_classic_link
            - enable_classic_link
            - get_available_subresources
            - modify_attribute
            - request_vpc_peering_connection
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, name)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "Vpc",
        action,
        resource_id=vpc.vpc_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
