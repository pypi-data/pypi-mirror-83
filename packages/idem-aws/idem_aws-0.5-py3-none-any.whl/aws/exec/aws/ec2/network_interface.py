"""
EC2 Network Interface
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, subnet: str, **kwargs):
    """
    :param name: The name of the network_interface to create, this will be defined in it's unique tag
    :param subnet: The name of the subnet within which to create an network_interface
    :param kwargs: Any additional arguments to pass to the Subnet().create_network_interfaces() function
    """
    _, subnet = await hub.exec.aws.ec2.subnet.get(ctx, subnet)

    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_network_interface",
        dry_run=ctx.get("test", False),
        subnet_id=subnet.subnet_id,
        **kwargs,
    )
    if not status:
        return status, ret
    await hub.exec.aws.ec2.tag.create(
        ctx,
        resource_id=ret.network_interface.network_interface_id,
        tags={ctx.acct.provider_tag_key: name},
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs):
    _, network_interface = await hub.exec.aws.ec2.network_interface.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_network_interface",
        network_interface_id=network_interface.network_interface_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str):
    status, network_interfaces = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_network_interfaces",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )

    if not status or not len(network_interfaces.network_interfaces):
        return False, {}

    network_interface = network_interfaces.network_interfaces[0]
    network_interface.name = name
    network_interface.tags = hub.tool.aws.dict.flatten_tags(
        {"tags": network_interface.pop("tag_set")}
    ).tags
    return True, network_interface


async def list_(hub, ctx, **kwargs):
    status, result = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_network_interfaces",
        dry_run=ctx.get("test", False),
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}]
        + kwargs.pop("filters", []),
        **kwargs,
    )
    if not status:
        return status, result

    # TODO paginate results
    ret = {}
    for network_interface in result.get("network_interfaces", []):
        network_interface.update(
            hub.tool.aws.dict.flatten_tags({"tags": network_interface.pop("tag_set")})
        )
        network_interface.name = network_interface.tags[ctx.acct.provider_tag_key]
        ret[network_interface.name] = network_interface

    # Flatten the list information
    return status, {"network_interfaces": ret}


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, network_interface = await hub.exec.aws.ec2.network_interface.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=network_interface.network_interface_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs):
    _, network_interface = await hub.exec.aws.ec2.network_interface.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx,
        resource_id=network_interface.network_interface_id,
        resource_type="network-interface",
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, network_interface = await hub.exec.aws.ec2.network_interface.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=network_interface.network_interface_id,
        keys=keys,
        resource_type="network-interface",
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The network_interface name
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - assign_private_ip_addresses
            - attach
            - describe_attribute
            - detach
            - get_available_subresources
            - modify_attribute
            - reset_attribute
            - unassign_private_ip_addresses
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, network_interface = await hub.exec.aws.ec2.network_interface.get(ctx, name)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "NetworkInterface",
        action,
        resource_id=network_interface.network_interface_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
