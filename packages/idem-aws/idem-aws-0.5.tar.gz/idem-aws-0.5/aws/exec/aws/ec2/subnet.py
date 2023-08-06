"""
EC2 Subnet
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_subnets",
        dry_run=ctx.get("test", False),
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}],
    )


async def create(hub, ctx, name: str, cidr_block: str, vpc: str, **kwargs):
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, vpc)
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_subnet",
        cidr_block=cidr_block,
        vpc_id=vpc.vpc_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    if not status:
        return status, ret
    await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=ret.subnet.subnet_id, tags={ctx.acct.provider_tag_key: name}
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs):
    _, subnet = await hub.exec.aws.ec2.subnet.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_subnet",
        subnet_id=subnet.subnet_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str):
    status, subnets = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_subnets",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )

    if not status or not len(subnets.subnets):
        return False, {}

    subnet = subnets.subnets[0]
    subnet.name = name
    return True, subnet


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, subnet = await hub.exec.aws.ec2.subnet.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=subnet.subnet_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs):
    _, subnet = await hub.exec.aws.ec2.subnet.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx, resource_id=subnet.subnet_id, resource_type="subnet", **kwargs
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, subnet = await hub.exec.aws.ec2.subnet.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx, resource_id=subnet.subnet_id, keys=keys, resource_type="subnet", **kwargs
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, subnet = await hub.exec.aws.ec2.subnet.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="modify_subnet_attribute",
        subnet_id=subnet.subnet_id,
        **kwargs,
    )
