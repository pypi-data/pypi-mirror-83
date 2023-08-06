from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_internet_gateway",
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    if not status:
        return status, ret

    await hub.exec.aws.ec2.tag.create(
        ctx,
        resource_id=ret.internet_gateway.internet_gateway_id,
        tags={ctx.acct.provider_tag_key: name},
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, internet_gateway = await hub.exec.aws.ec2.internet_gateway.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_internet_gateway",
        internet_gateway_id=internet_gateway.internet_gateway_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, internet_gateways = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_internet_gateways",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
        **kwargs,
    )

    if not status or not len(internet_gateways.internet_gateways):
        return False, {}

    internet_gateway = internet_gateways.internet_gateways[0]
    internet_gateway.name = name
    return True, internet_gateway


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_internet_gateways",
        dry_run=ctx.get("test", False),
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}],
        **kwargs,
    )


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, internet_gateway = await hub.exec.aws.ec2.internet_gateway.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=internet_gateway.internet_gateway_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, internet_gateway = await hub.exec.aws.ec2.internet_gateway.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx,
        resource_id=internet_gateway.internet_gateway_id,
        resource_type="internet-gateway",
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, internet_gateway = await hub.exec.aws.ec2.internet_gateway.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=internet_gateway.internet_gateway_id,
        keys=keys,
        resource_type="internet-gateway",
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, vpc: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The internet_gateway name
    :param vpc: The name of a vpc to attach or detach
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - attach_to_vpc
            - detach_from_vpc
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, internet_gateway = await hub.exec.aws.ec2.internet_gateway.get(ctx, name)
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, vpc)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "InternetGateway",
        action,
        resource_id=internet_gateway.internet_gateway_id,
        vpc_id=vpc.vpc_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
