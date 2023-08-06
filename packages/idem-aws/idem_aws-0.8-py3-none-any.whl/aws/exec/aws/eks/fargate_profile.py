# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    cluster: str,
    role: str,
    subnets: List[str] = None,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    status, role = await hub.exec.aws.iam.role.get(ctx, role)

    if not status:
        return status, role

    subnet_ids = []
    for subnet in subnets or ():
        status, subnet = await hub.exec.aws.ec2.subnet.get(ctx, subnet)
        if not status:
            return status, subnet
        subnet_ids.append(subnet.subnet_id)

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="create_fargate_profile",
        fargate_profile_name=name,
        cluster_name=cluster,
        pod_execution_role_arn=role.arn,
        subnets=subnet_ids,
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
        func="delete_fargate_profile",
        fargate_profile_name=name,
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
        func="describe_fargate_profile",
        fargate_profile_name=name,
        cluster_name=cluster,
        dromedary=True,
        **kwargs,
    )


async def list_(hub, ctx, cluster: str, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    status, fargate_profiles = await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="list_fargate_profiles",
        dromedary=True,
        cluster_name=cluster,
        **kwargs,
    )
    # TODO paginate results
    return status, fargate_profiles


async def tag(
    hub, ctx, name: str, cluster: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, fargate_profile = await hub.exec.aws.eks.fargate_profile.get(
        ctx, name, cluster=cluster
    )

    if not status:
        return status, fargate_profile

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="tag_resource",
        resource_arn=fargate_profile.fargate_profile_arn,
        tags=tags,
        dromedary=True,
        **kwargs,
    )


async def tags(
    hub, ctx, name: str, cluster: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, fargate_profile = await hub.exec.aws.eks.fargate_profile.get(
        ctx, name, cluster=cluster
    )

    if not status:
        return status, fargate_profile

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="list_tags_for_resource",
        resource_arn=fargate_profile.fargate_profile_arn,
        dromedary=True,
        **kwargs,
    )


async def untag(
    hub, ctx, name: str, cluster: str, keys: List[str], **kwargs
) -> Tuple[bool, Any]:
    status, fargate_profile = await hub.exec.aws.eks.fargate_profile.get(
        ctx, name, cluster=cluster
    )

    if not status:
        return status, fargate_profile

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="untag_resource",
        resource_arn=fargate_profile.fargate_profile_arn,
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
    raise NotImplementedError()
