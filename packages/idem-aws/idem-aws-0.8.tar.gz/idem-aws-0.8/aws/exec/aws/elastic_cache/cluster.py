from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="create_cache_cluster",
        cache_cluster_id=name,
        tags=[{"Key": ctx.acct.provider_tag_key, "Value": name}],
        **kwargs,
    )


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="delete_cache_cluster",
        cache_cluster_id=name,
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        max_records=1,
        show_cache_node_info=True,
        func="describe_cache_clusters",
        cache_cluster_id=name,
        **kwargs,
    )
    return status, ret


async def list_(
    hub, ctx, max_records: int = 100, **kwargs
) -> Tuple[bool, List[Dict[str, Any]]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="elasticache",
        func="describe_cache_clusters",
        max_records=max_records,
        **kwargs,
    )


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
