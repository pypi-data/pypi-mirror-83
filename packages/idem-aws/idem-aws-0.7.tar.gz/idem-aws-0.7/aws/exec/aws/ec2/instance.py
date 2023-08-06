"""
EC2 Instance
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, subnet: str, **kwargs):
    """
    :param name: The name of the instance to create, this will be defined in it's unique tag
    :param subnet: The name of the subnet within which to create an instance
    :param kwargs: Any additional arguments to pass to the Subnet().create_instances() function
    """
    _, subnet = await hub.exec.aws.ec2.subnet.get(ctx, subnet)
    status, ret = await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "Subnet",
        "create_instances",
        resource_id=subnet.subnet_id,
        dry_run=ctx.get("test", False),
        # Only launch create one instance at a time so that names stay unique
        min_count=1,
        max_count=1,
        tag_specifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": ctx.acct.provider_tag_key, "Value": name}],
            }
        ]
        + kwargs.pop("tag_specifications", []),
        **kwargs,
    )
    if status is False or not len(ret):
        return False, ret
    instance = ret[0]
    # TODO what things should happen with the instance object here now that hit has been created?
    # TODO is this where we leverage heist to boostrap salt?
    if kwargs.get("start"):
        instance.start()

    return True, instance.meta.data


async def delete(hub, ctx, name: str, **kwargs):
    _, instance = await hub.exec.aws.ec2.instance.get(ctx, name)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "Instance",
        "terminate",
        resource_id=instance.instance_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str):
    status, instances = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_instances",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )

    if (
        not status
        or not len(instances.reservations)
        or not len(instances.reservations[0].instances)
    ):
        return False, {}

    reservation = instances.reservations[0]
    instance = reservation.pop("instances")[0]
    instance.reservation = reservation
    instance.name = name
    return True, instance


async def list_(hub, ctx, **kwargs):
    status, result = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_instances",
        dry_run=ctx.get("test", False),
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}]
        + kwargs.pop("filters", []),
        **kwargs,
    )
    if not status:
        return status, result

    # TODO paginate results
    ret = []

    # Flatten the list information
    for reservation in result.get("reservations", ()):
        instances = reservation.pop("instances", ())
        for instance in instances:
            instance.reservation = reservation
            name = instance.tags.get(ctx.acct.provider_tag_key)
            if name:
                # Don't include resources that aren't tagged with the provider tag key
                instance.name = name
                ret.append(instance)

    return status, {"instances": ret}


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, instance = await hub.exec.aws.ec2.instance.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=instance.instance_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs):
    _, instance = await hub.exec.aws.ec2.instance.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx, resource_id=instance.instance_id, resource_type="instance", **kwargs
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, instance = await hub.exec.aws.ec2.instance.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=instance.instance_id,
        resource_type="instance",
        keys=keys,
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The instance name
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - attach_classic_link_vpc
            - attach_volume
            - console_output
            - create_image
            - describe_attribute
            - detach_classic_link_vpc
            - detach_volume
            - get_available_subresources
            - load
            - modify_attribute
            - monitor
            - password_data
            - reboot
            - reload
            - report_status
            - reset_attribute
            - reset_kernel
            - reset_ramdisk
            - reset_source_dest_check
            - start
            - stop
            - unmonitor
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, instance = await hub.exec.aws.ec2.instance.get(ctx, name)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "Instance",
        action,
        resource_id=instance.instance_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
