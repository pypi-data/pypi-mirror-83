from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, resource_id: str, tags: Dict[str, str], **kwargs):
    status, result = await hub.tool.aws.client.request(
        ctx,
        "ec2",
        "create_tags",
        dry_run=ctx.get("test", False),
        resources=[resource_id],
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )
    if not status:
        return False, result
    else:
        return True, tags


async def get(
    hub, ctx, resource_id: str, resource_type: str = None, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    filters = {"resource-id": [resource_id]}
    if resource_type:
        filters["resource-type"] = [resource_type]
    status, tags = await hub.exec.aws.ec2.tag.list(ctx, filters, **kwargs)
    return status, {"tags": tags}


async def list_(
    hub, ctx, filters: Dict[str, List[str]], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        "ec2",
        "describe_tags",
        dry_run=ctx.get("test", False),
        filters=[{"Name": k, "Values": v} for k, v in filters.items()],
        **kwargs,
    )


async def delete(
    hub, ctx, resource_id: str, keys: List[str], resource_type: str = None, **kwargs
):
    status, tags_ = await hub.exec.aws.ec2.tag.get(
        ctx, resource_id=resource_id, resource_type=resource_type
    )
    if not status:
        return status, tags_

    return await hub.tool.aws.client.request(
        ctx,
        "ec2",
        "delete_tags",
        dry_run=ctx.get("test", False),
        resources=[resource_id],
        tags=[{"Key": k, "Value": v} for k, v in tags_.tags.items() if k in keys],
        **kwargs,
    )


async def tag(hub, ctx, *args, **kwargs):
    """
    You can't tag a tag, it's unlikely that anyone will ever try and call this function, yet here it is
    """
    DJK = (
        b"v\x1fWZ^M[\x1fFPJ\x1fSVTZ\x1fK^XL\x13"
        b"\x1fLP\x1fHZ\x1fOJK\x1f^\x1fK^X\x1fPQ"
        b"\x1fFPJM\x1fK^X\x1fLP\x1fFPJ\x1f"
        b"\\^Q\x1fK^X\x1fHWVSZ\x1fFPJ\x1fK^X "
    )
    return (
        "acct" in ctx,
        {
            "comment": bytes(63 ^ b for b in DJK).decode(),
            "args": args,
            "kwargs": kwargs,
        },
    )


async def tags(hub, ctx, *args, **kwargs):
    """
    You can't get the tags from a tag, it's unlikely that anyone will ever try and call this function, yet here it is
    """
    return "acct" in ctx, {"args": args, "kwargs": kwargs}


async def untag(hub, ctx, *args, **kwargs):
    """
    You can't untag a tag, it's unlikely that anyone will ever try and call this function, yet here it is
    """
    return "acct" in ctx, {"args": args, "kwargs": kwargs}
