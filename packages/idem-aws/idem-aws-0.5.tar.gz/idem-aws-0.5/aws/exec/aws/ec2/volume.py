from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub, ctx, name: str, availability_zone: str, size: int, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_volume",
        dry_run=ctx.get("test", False),
        availability_zone=availability_zone,
        size=size,
        tag_specifications=[
            {
                "ResourceType": "volume",
                "Tags": [{"Key": ctx.acct.provider_tag_key, "Value": name}],
            }
        ]
        + kwargs.get("tag_specifications", []),
        **kwargs,
    )


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, volume = await hub.exec.aws.ec2.volume.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx, client="ec2", func="delete_volume", volume_id=volume.volume_id, **kwargs
    )


async def get(hub, ctx, name: str) -> Tuple[bool, Dict[str, Any]]:
    status, volumes = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_volumes",
        dry_run=ctx.get("test", False),
        max_results=1,
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )
    if len(volumes.volumes):
        volume = volumes.volumes[0]
        volume.name = name
        return status, volume
    else:
        return False, {}


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_volumes",
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}],
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, volume = await hub.exec.aws.ec2.volume.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=volume.volume_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs):
    _, volume = await hub.exec.aws.ec2.volume.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx, resource_id=volume.volume_id, resource_type="volume", **kwargs
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, volume = await hub.exec.aws.ec2.volume.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx, resource_id=volume.volume_id, keys=keys, resource_type="volume", **kwargs
    )


async def update(
    hub, ctx, action: str, name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The volume name
    :param action: The resource action to perform.
        Available actions are:
            - associate_dhcp_options
            - attach_to_instance
            - create_snapshot
            - detach_from_instance
            - enable_io
            - modify_attribute
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, volume = await hub.exec.aws.ec2.volume.get(ctx, name)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "Volume",
        action,
        resource_id=volume.volume_id,
        **kwargs,
    )
