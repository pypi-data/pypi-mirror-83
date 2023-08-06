from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub, ctx, name: str, assume_role_policy_document: str, tags: List = None, **kwargs
):
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="create_role",
        role_name=name,
        assume_role_policy_document=assume_role_policy_document,
        tags=[{"Key": ctx.acct.provider_tag_key, "Value": name}] + (tags or []),
        **kwargs,
    )
    return status, ret.get("role", {})


async def delete(hub, ctx, name):
    return await hub.tool.aws.client.request(
        ctx, client="iam", func="delete_role", role_name=name
    )


async def get(hub, ctx, name: str):
    status, l = await hub.exec.aws.iam.role.list(ctx)
    item = l.get(name)
    if item:
        item["name"] = name
        return True and status, item
    else:
        return False, item


async def list_(hub, ctx, **kwargs):
    ret = []
    status, roles = await hub.tool.aws.client.request(
        ctx, client="iam", func="list_roles", **kwargs
    )
    if not status:
        return status, roles
    for role in roles.get("roles", []):
        name = role["role_name"]
        _, tags = await hub.tool.aws.client.request(
            ctx, client="iam", func="list_role_tags", role_name=name
        )
        role["tags"] = tags.get("tags", {})
        ret.append(role)
    return status, {"roles": ret}


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="tag_role",
        role_name=name,
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="list_role_tags",
        role_name=name,
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="untag_role",
        role_name=name,
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="iam",
        func="update_role",
        role_name=name,
        **kwargs,
    )
