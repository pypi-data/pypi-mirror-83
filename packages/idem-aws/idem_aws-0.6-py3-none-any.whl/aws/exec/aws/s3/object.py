from typing import Dict

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx, bucket: str, version_id: str = None, **kwargs):
    ret = []
    status, objects = await hub.tool.aws.client.request(
        ctx, client="s3", func="list_objects_v2", bucket=bucket, **kwargs
    )
    if not status:
        return status, objects
    for o in objects.get("contents", []):
        name = o.key
        o.bucket = objects.name
        _, o.tags = await hub.exec.aws.s3.object.tags(
            ctx, name, bucket, version_id=version_id
        )
        ret.append(o)
    return status, hub.tool.aws.dict.flatten_tags({"objects": ret})


async def create(
    hub,
    ctx,
    name: str,
    bucket: str,
    **kwargs,
):
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="s3",
        func="put_object",
        key=name,
        bucket=bucket,
        **kwargs,
    )
    await hub.exec.aws.s3.object.tag(
        ctx, name, bucket=bucket, tags={ctx.acct.provider_tag_key: name}
    )
    return status, ret


async def delete(hub, ctx, name: str, bucket: str):
    return await hub.tool.aws.client.request(
        ctx,
        client="s3",
        func="delete_object",
        key=name,
        bucket=bucket,
    )


async def get(hub, ctx, name: str, bucket: str, version_id: str = None, **kwargs):
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="s3",
        func="get_object",
        key=name,
        bucket=bucket,
        version_id=version_id,
        **kwargs,
    )
    if not status:
        return status, ret

    ret.name = name
    _, ret.tags = await hub.exec.aws.s3.object.tags(
        ctx, name, bucket=bucket, version_id=version_id
    )

    return status, ret


async def tag(hub, ctx, name: str, bucket: str, tags: Dict[str, str]):
    status, existing_tags = await hub.exec.aws.s3.object.tags(ctx, name, bucket=bucket)
    if status:
        new_tags = existing_tags
        new_tags.update(tags)
    else:
        new_tags = tags
    return await hub.tool.aws.client.request(
        ctx,
        client="s3",
        func="put_object_tagging",
        key=name,
        bucket=bucket,
        tagging={"TagSet": [{"Key": k, "Value": v} for k, v in new_tags.items()]},
    )


async def tags(hub, ctx, name: str, bucket: str, **kwargs):
    return await hub.tool.aws.client.request(
        ctx, client="s3", func="get_object_tagging", key=name, bucket=bucket, **kwargs
    )
