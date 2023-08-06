from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub, ctx, name: str, source: str = None, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param name: The name of the key pair
    :param source: The path to a file containing a public key
    """
    if source:
        with open(source, "rb") as fh:
            status, ret = await hub.tool.aws.client.request(
                ctx,
                client="ec2",
                func="import_key_pair",
                public_key_material=fh.read(),
                dry_run=ctx.get("test", False),
                key_name=name,
                **kwargs,
            )
    else:
        status, ret = await hub.tool.aws.client.request(
            ctx,
            client="ec2",
            func="create_key_pair",
            dry_run=ctx.get("test", False),
            key_name=name,
            **kwargs,
        )
    if not status:
        return status, ret

    await hub.exec.aws.ec2.tag.create(
        ctx,
        resource_id=ret.key_fingerprint,
        tags={ctx.acct.provider_tag_key: name},
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_key_pair",
        key_name=name,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(hub, ctx, name: str) -> Tuple[bool, Dict[str, Any]]:
    status, key_pairs = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_key_pairs",
        dry_run=ctx.get("test", False),
        filters=[{"Name": "key-name", "Values": [name]}],
    )

    if not status or not len(key_pairs.key_pairs):
        return False, {}

    key_pair = key_pairs.key_pairs[0]
    key_pair.name = name
    _, t = await hub.exec.aws.ec2.tag.get(
        ctx,
        resource_id=key_pair.get("key_pair_id", key_pair.get("key_fingerprint", name)),
        resource_type="key-pair",
    )
    key_pair.tags = t.tags
    return True, key_pair


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    l = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_key_pairs",
        dry_run=ctx.get("test", False),
        **kwargs,
    )
    return l


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, key_pair = await hub.exec.aws.ec2.key_pair.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=key_pair.key_pair_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, key_pair = await hub.exec.aws.ec2.key_pair.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx, resource_id=key_pair.key_pair_id, resource_type="key-pair", **kwargs
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, key_pair = await hub.exec.aws.ec2.key_pair.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=key_pair.key_pair_id,
        keys=keys,
        resource_type="key-pair",
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, vpc: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The key_pair name
    :param vpc: The name of a vpc to attach or detach
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - attach_to_vpc
            - detach_from_vpc
    :param kwargs: keyword arguments to pass to the resource action
    """
    _, key_pair = await hub.exec.aws.ec2.key_pair.get(ctx, name)
    _, vpc = await hub.exec.aws.ec2.vpc.get(ctx, vpc)
    return await hub.tool.aws.resource.request(
        ctx,
        "ec2",
        "InternetGateway",
        action,
        resource_id=key_pair.key_pair_id,
        vpc_id=vpc.vpc_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
