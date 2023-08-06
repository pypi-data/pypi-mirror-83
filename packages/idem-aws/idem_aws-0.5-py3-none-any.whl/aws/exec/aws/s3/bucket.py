from typing import Dict

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    ret = []
    status, buckets = await hub.tool.aws.client.request(
        ctx, client="s3", func="list_buckets"
    )
    if not status:
        return status, buckets
    for bucket in buckets.get("buckets", []):
        _, bucket.tags = await hub.exec.aws.s3.bucket.tags(ctx, bucket.name)
        ret.append(bucket)
    return status, hub.tool.aws.dict.flatten_tags({"buckets": ret})


async def create(
    hub,
    ctx,
    name: str,
    **kwargs,
):
    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="s3",
        func="create_bucket",
        bucket=name,
        **kwargs,
    )
    await hub.exec.aws.s3.bucket.tag(ctx, name, tags={ctx.acct.provider_tag_key: name})
    return status, ret


async def delete(hub, ctx, name: str):
    return await hub.tool.aws.client.request(
        ctx, client="s3", func="delete_bucket", Bucket=name
    )


async def get(hub, ctx, name: str):
    status, l = await hub.exec.aws.s3.bucket.list(ctx)
    item = l.get(name)
    if item:
        item["name"] = name
        return True and status, item
    else:
        return False, item


async def tag(hub, ctx, name: str, tags: Dict[str, str]):
    status, existing_tags = await hub.exec.aws.s3.bucket.tags(ctx, name)
    if status:
        new_tags = existing_tags
        new_tags.update(tags)
    else:
        new_tags = tags
    return await hub.tool.aws.client.request(
        ctx,
        client="s3",
        func="put_bucket_tagging",
        bucket=name,
        tagging={"TagSet": [{"Key": k, "Value": v} for k, v in new_tags.items()]},
    )


async def tags(hub, ctx, name: str):
    return await hub.tool.aws.client.request(
        ctx, client="s3", func="get_bucket_tagging", bucket=name
    )
