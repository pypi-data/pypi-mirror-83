from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    replication_group: str = None,
    cluster: str = None,
    kms_key: str = None,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    if replication_group:
        _, replication_group = await hub.exec.aws.elastic_cache.replication_group.get(
            ctx, replication_group
        )
        kwargs["replication_group_id"] = replication_group.replication_group_id
    if cluster:
        _, cluster = await hub.exec.aws.elastic_cache.cluster.get(ctx, cluster)
        kwargs["cache_cluster_id"] = cluster.cach_cluster_id
    if kms_key:
        _, kms_key = await hub.exec.aws.kms.key.get(ctx, kms_key)
        kwargs["kms_key_id"] = kms_key.kms_key_id
    return await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="create_snapshot",
        snapshot_name=name,
        **kwargs,
    )


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="delete_snapshot",
        snapshot_name=name,
        **kwargs,
    )


async def get(
    hub, ctx, name: str, replication_group: str = None, cluster: str = None, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    if replication_group:
        _, replication_group = await hub.exec.aws.elastic_cache.replication_group.get(
            ctx, replication_group
        )
        kwargs["replication_group_id"] = replication_group.replication_group_id
    if cluster:
        _, cluster = await hub.exec.aws.elastic_cache.cluster.get(ctx, cluster)
        kwargs["cache_cluster_id"] = cluster.cach_cluster_id
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        snapshot_name=name,
        max_records=1,
        show_node_group_config=True,
        func="describe_snapshots",
        **kwargs,
    )
    return status, ret


async def list_(
    hub,
    ctx,
    replication_group: str = None,
    cluster: str = None,
    max_records: int = 50,
    **kwargs,
) -> Tuple[bool, List[Dict[str, Any]]]:
    if replication_group:
        _, replication_group = await hub.exec.aws.elastic_cache.replication_group.get(
            ctx, replication_group
        )
        kwargs["replication_group_id"] = replication_group.replication_group_id
    if cluster:
        _, cluster = await hub.exec.aws.elastic_cache.cluster.get(ctx, cluster)
        kwargs["cache_cluster_id"] = cluster.cach_cluster_id
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        max_records=max_records,
        show_node_group_config=True,
        func="describe_snapshots",
        **kwargs,
    )
    return status, ret


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="add_tags_to_resource",
        resource_name=name,
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="list_tags_for_resource",
        resource_name=name,
        **kwargs,
    )
    return status, {"tags": ret}


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    return await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="remove_tags_from_resource",
        resource_name=name,
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="TODO_UPDATE_FUNC",
        name=name,
        **kwargs,
    )
