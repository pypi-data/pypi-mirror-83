"""
EC2 Image
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub, ctx, name: str, instance, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param name: The name of the ami to create (This will be assigned to it's unique tag)
    :param instance: The name of the ec2 instance to use based on it's unique tag
    """
    _, instance = await hub.exec.aws.ec2.instance.get(ctx, instance)
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_image",
        name=name,
        instance_id=instance.instance_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=ret.image_id, tags={ctx.acct.provider_tag_key: name}
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, image = await hub.exec.aws.ec2.image.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="deregister_image",
        image_id=image.image_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, images = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_images",
        dry_run=ctx.get("test", False),
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
        **kwargs,
    )

    if not status or not len(images.images):
        return False, {}

    image = images.images[0]
    # TODO Document this, we are mixing things up from what the api does
    image.image = image.name
    image.name = name
    return True, image


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    status, result = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_images",
        dry_run=ctx.get("test", False),
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}]
        + kwargs.pop("filters", []),
        **kwargs,
    )
    if not status:
        return status, result

    # TODO paginate results
    ret = []

    for image in result.images:
        name = image.tags.get(ctx.acct.provider_tag_key)
        if name:
            # TODO Document this, we are mixing things up from what the api does
            image.image = image.name
            image.name = name
            ret.append(image)

    return status, {"images": ret}


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, image = await hub.exec.aws.ec2.image.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=image.image_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, image = await hub.exec.aws.ec2.image.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx, resource_id=image.image_id, resource_type="image", **kwargs
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, image = await hub.exec.aws.ec2.image.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx, resource_id=image.image_id, keys=keys, resource_type="image", **kwargs
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, image = await hub.exec.aws.ec2.image.get(ctx, name)
    # TODO add documentation for what "modify_image_attribute" can do
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="modify_image_attribute",
        image_id=image.image_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
