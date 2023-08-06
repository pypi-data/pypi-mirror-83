# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html
# https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html
# https://zacharyloeber.com/2020/05/aws-testing-with-localstack-on-kubernetes/
# https://medium.com/@alejandro.millan.frias/managing-kubernetes-from-aws-lambda-7922c3546249
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    role: str,
    subnets: List[str] = None,
    security_groups: List[str] = None,
    endpoint_public_access: bool = True,
    endpoint_private_access: bool = False,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    status, role = await hub.exec.aws.iam.role.get(ctx, role)

    if not status:
        return status, role

    resources_vpc_config = await hub.tool.aws.config.vpc_resource(
        ctx,
        dromedary=True,
        subnets=subnets,
        security_groups=security_groups,
        endpoint_public_access=endpoint_public_access,
        endpoint_private_access=endpoint_private_access,
    )

    if not resources_vpc_config:
        return False, resources_vpc_config

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="create_cluster",
        name=name,
        role_arn=role.arn,
        resources_vpc_config=resources_vpc_config,
        # TODO also use tags from kwargs
        tags={ctx.acct.provider_tag_key: name},
        dromedary=True,
        **kwargs,
    )


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="delete_cluster",
        name=name,
        dromedary=True,
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="describe_cluster",
        name=name,
        dromedary=True,
        **kwargs,
    )


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    status, clusters = await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="list_clusters",
        dromedary=True,
        **kwargs,
    )
    # TODO paginate results
    return status, clusters


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, cluster = await hub.exec.aws.eks.cluster.get(ctx, name)

    if not status:
        return status, cluster

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="tag_resource",
        resource_arn=cluster.arn,
        tags=tags,
        dromedary=True,
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, cluster = await hub.exec.aws.eks.cluster.get(ctx, name)

    if not status:
        return status, cluster

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="list_tags_for_resource",
        resource_arn=cluster.arn,
        dromedary=True,
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    status, cluster = await hub.exec.aws.eks.cluster.get(ctx, name)

    if not status:
        return status, cluster

    return await hub.tool.aws.client.request(
        ctx,
        client="eks",
        func="untag_resource",
        resource_arn=cluster.arn,
        tag_keys=keys,
        dromedary=True,
        **kwargs,
    )


async def update(
    hub,
    ctx,
    name: str,
    subnets: List[str] = None,
    security_groups: List[str] = None,
    endpoint_public_access: bool = True,
    endpoint_private_access: bool = False,
    public_access_cidrs: List[str] = None,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    resources_vpc_config = await hub.tool.aws.config.vpc_resource(
        ctx,
        dromedary=True,
        subnets=subnets,
        security_groups=security_groups,
        endpoint_public_access=endpoint_public_access or [],
        endpoint_private_access=endpoint_private_access or [],
        public_access_cidrs=public_access_cidrs or [],
    )

    if not resources_vpc_config:
        return False, resources_vpc_config

    return await hub.tool.aws.client.request(
        ctx,
        dromedary=True,
        client="eks",
        func="update_cluster_config",
        name=name,
        resources_vpc_config=resources_vpc_config,
        **kwargs,
    )
