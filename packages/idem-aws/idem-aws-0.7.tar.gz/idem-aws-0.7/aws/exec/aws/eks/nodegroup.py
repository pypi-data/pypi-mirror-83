# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    cluster: str,
    min_size: int = None,
    max_size: int = None,
    desired_size: int = None,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="create_nodegroup",
        node_group_name=name,
        cluster_name=cluster,
        scaling_config=await hub.tool.aws.config.scaling(
            min_size=min_size, max_size=max_size, desired_size=desired_size
        ),
        dromedary=True,
        # TODO also use tags from kwargs
        tags={ctx.acct.provider_tag_key: name},
        **kwargs,
    )


async def delete(
    hub, ctx, name: str, cluster: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="delete_nodegroup",
        node_group_name=name,
        cluster_name=cluster,
        dromedary=True,
        **kwargs,
    )


async def get(
    hub, ctx, name: str, cluster: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="describe_nodegroup",
        node_group_name=name,
        cluster_name=cluster,
        dromedary=True,
        **kwargs,
    )


async def list_(hub, ctx, cluster: str, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    status, nodegroups = await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="list_nodegroups",
        dromedary=True,
        cluster_name=cluster,
        **kwargs,
    )
    # TODO paginate results
    return status, nodegroups


async def tag(
    hub, ctx, name: str, cluster: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, nodegroup = await hub.exec.aws.eks.nodegroup.get(ctx, name, cluster=cluster)

    if not status:
        return status, nodegroup

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="tag_resource",
        resource_arn=nodegroup.nodegroup_arn,
        tags=tags,
        dromedary=True,
        **kwargs,
    )


async def tags(
    hub, ctx, name: str, cluster: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, nodegroup = await hub.exec.aws.eks.nodegroup.get(ctx, name, cluster=cluster)

    if not status:
        return status, nodegroup

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="list_tags_for_resource",
        resource_arn=nodegroup.nodegroup_arn,
        dromedary=True,
        **kwargs,
    )


async def untag(
    hub, ctx, name: str, cluster: str, keys: List[str], **kwargs
) -> Tuple[bool, Any]:
    status, nodegroup = await hub.exec.aws.eks.nodegroup.get(ctx, name, cluster=cluster)

    if not status:
        return status, nodegroup

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="untag_resource",
        resource_arn=nodegroup.nodegroup_arn,
        tag_keys=keys,
        dromedary=True,
        **kwargs,
    )


async def update(
    hub,
    ctx,
    name: str,
    cluster: str,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="update_nodegroup_config",
        node_group_name=name,
        cluster_name=cluster,
        dromedary=True,
        **kwargs,
    )
