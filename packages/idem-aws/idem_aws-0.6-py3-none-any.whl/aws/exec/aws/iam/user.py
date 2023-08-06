from typing import Any, Dict, List, Tuple

__func_alias__ = {
    "list_": "list",
}


async def create(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="create_user",
        user_name=name,
        tags=[{"Key": ctx.acct.provider_tag_key, "Value": name}]
        + kwargs.pop("tags", []),
        **kwargs,
    )


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="delete_user",
        user_name=name,
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, user = await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="get_user",
        user_name=name,
        **kwargs,
    )
    if not status:
        return status, user
    user.user.name = name
    return status, user.user


async def list_(hub, ctx, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    ret = []
    status, users = await hub.tool.aws.client.request(
        ctx, client="iam", func="list_users", **kwargs
    )
    if not status:
        return status, users

    for user in users.get("users", []):
        user.name = user.user_name
        _, user.tags = await hub.exec.aws.iam.user.tags(ctx, name=user.name)
        ret.append(user)

    return status, {"users": ret}


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="tag_user",
        user_name=name,
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="list_user_tags",
        user_name=name,
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="untag_user",
        user_name=name,
        tag_keys=keys,
        **kwargs,
    )


async def update(
    hub, ctx, action: str, name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param hub:
    :param ctx:
    :param name: The instance name
    :param action: The resource action to perform.
        At the time of writing, the available actions are:
            - add_group
            - attach_policy
            - create_access_key_pair
            - create_login_profile
            - create_policy
            - detach_policy
            - enable_mfa
            - get_available_subresources
            - remove_group
            - update
    :param kwargs: keyword arguments to pass to the resource action
    """
    status, ret = await hub.tool.aws.resource.request(
        ctx,
        "iam",
        "User",
        action,
        resource_id=name,
        **kwargs,
    )
    return status is not False, ret
