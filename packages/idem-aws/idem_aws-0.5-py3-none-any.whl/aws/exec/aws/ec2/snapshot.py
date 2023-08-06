"""
EC2 Snapshot
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub, ctx, name: str, volume: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    _, volume = await hub.exec.aws.ec2.volume.get(ctx, volume)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_snapshot",
        dry_run=ctx.get("test", False),
        volume_id=volume.volume_id,
        tag_specifications=[
            {
                "ResourceType": "snapshot",
                "Tags": [{"Key": ctx.acct.provider_tag_key, "Value": name}],
            }
        ]
        + kwargs.get("tag_specifications", []),
        **kwargs,
    )


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    _, snapshot = await hub.exec.aws.ec2.snapshot.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_snapshot",
        snapshot_id=snapshot.snapshot_id,
        **kwargs,
    )


async def get(hub, ctx, name: str) -> Tuple[bool, Dict[str, Any]]:
    status, snapshots = await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_snapshots",
        dry_run=ctx.get("test", False),
        max_results=1,
        filters=[{"Name": f"tag:{ctx.acct.provider_tag_key}", "Values": [name]}],
    )
    if len(snapshots.snapshots):
        snapshot = snapshots.snapshots[0]
        snapshot.name = name
        return status, snapshot
    else:
        return False, {}


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="describe_snapshots",
        filters=[{"Name": "tag-key", "Values": [ctx.acct.provider_tag_key]}],
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def tag(hub, ctx, name: str, tags: Dict[str, str], **kwargs):
    _, snapshot = await hub.exec.aws.ec2.snapshot.get(ctx, name)
    return await hub.exec.aws.ec2.tag.create(
        ctx, resource_id=snapshot.snapshot_id, tags=tags, **kwargs
    )


async def tags(hub, ctx, name: str, **kwargs):
    _, snapshot = await hub.exec.aws.ec2.snapshot.get(ctx, name)
    return await hub.exec.aws.ec2.tag.get(
        ctx, resource_id=snapshot.snapshot_id, resource_type="snapshot", **kwargs
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    _, snapshot = await hub.exec.aws.ec2.snapshot.get(ctx, name)
    return await hub.exec.aws.ec2.tag.delete(
        ctx,
        resource_id=snapshot.snapshot_id,
        keys=keys,
        resource_type="snapshot",
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The snapshot name
    :param kwargs: keyword arguments to pass to the modify_snapshot_attribute
    """
    _, snapshot = await hub.exec.aws.ec2.snapshot.get(ctx, name)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="modify_snapshot_attribute",
        snapshot_id=snapshot.snapshot_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )
