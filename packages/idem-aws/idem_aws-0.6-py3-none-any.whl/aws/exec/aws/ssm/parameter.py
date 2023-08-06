from typing import Dict, List

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx, **kwargs):
    ret = []
    status, parameters = await hub.tool.aws.client.request(
        ctx, client="ssm", func="describe_parameters", **kwargs
    )
    if not status:
        return status, parameters
    for parameter in parameters.get("parameters", []):
        _, parameter.tags = await hub.exec.aws.ssm.parameter.tags(ctx, parameter.name)
        ret.append(parameter)
    return status, hub.tool.aws.dict.flatten_tags({"parameters": ret})


async def create(
    hub,
    ctx,
    name: str,
    value: str,
    type_: str = None,
    tags: List[str] = None,
    **kwargs,
):
    type_ = kwargs.pop("type", type_)
    if type_:
        type_ = hub.tool.aws.dict.camel(type_)
        assert type_ in ("String", "StringList", "SecureString")
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="ssm",
        func="put_parameter",
        name=name,
        value=value,
        type=type_,
        **kwargs,
    )
    # Tagging is possible in the create, but doesn't work as well as this
    await hub.exec.aws.ssm.parameter.tag(
        ctx, name=name, tags={ctx.acct.provider_tag_key: name}
    )
    return status, ret


async def delete(hub, ctx, name: str):
    return await hub.tool.aws.client.request(
        ctx, client="ssm", func="delete_parameter", name=name
    )


async def get(hub, ctx, name: str, **kwargs):
    status, ret = await hub.tool.aws.client.request(
        ctx, client="ssm", func="get_parameter", name=name, **kwargs
    )
    if not status:
        return status, ret

    _, tags = await hub.tool.aws.client.request(
        ctx,
        client="ssm",
        func="list_tags_for_resource",
        resource_type="Parameter",
        resource_id=ret.parameter.name,
    )
    _, ret.parameter.tags = await hub.exec.aws.ssm.parameter.tags(ctx, name)
    return status, ret.parameter


async def tag(hub, ctx, name: str, tags: Dict[str, str]):
    return await hub.tool.aws.client.request(
        ctx,
        client="ssm",
        func="add_tags_to_resource",
        resource_type="Parameter",
        resource_id=name,
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
    )


async def tags(hub, ctx, name: str):
    return await hub.tool.aws.client.request(
        ctx,
        client="ssm",
        func="list_tags_for_resource",
        resource_type="Parameter",
        resource_id=name,
    )
