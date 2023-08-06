from typing import Any, Dict, List, Tuple
from datetime import datetime

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    name: str,
    origins: Dict[str, Any],
    target_origin: str,
    signed_urls: bool = True,
    default_root_object: str = "index.html",
    trusted_signers: List[str] = None,
    cname_aliases: List[str] = None,
    distribution_config: Dict[str, Any] = None,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    """
    :param name:
    :param signed_urls: Specifies whether you want to require viewers to use signed URLs to access the files specified
    :param default_root_object: The object that you want CloudFront to request from your origin
    :param origins: A dictionary that contains an id (a unique identifier for the origin) mapped to a dict of values:
        - domain_name: The domain name for the origin
        - origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.
        - custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin
        - s3_origin_config: Use this type to specify an origin that is an Amazon S3 bucket that is * not * configured with static website hosting
    :param cname_aliases:
    :param kwargs:
    :return:
    """
    if cname_aliases is None:
        cname_aliases = []
    if distribution_config is None:
        distribution_config = {}
    if trusted_signers is None:
        trusted_signers = []

    distribution_config["Comment"] = "ok"
    distribution_config["Enabled"] = True
    distribution_config["CallerReference"] = str(datetime.now())
    distribution_config["Aliases"] = {
        "Quantity": len(cname_aliases),
        "Items": cname_aliases,
    }
    distribution_config["DefaultRootObject"] = default_root_object
    distribution_config["Origins"] = {
        "Quantity": len(origins),
        "Items": [
            {
                "Id": key,
                "DomainName": value.get("domain_name"),
                "CustomHeaders": {
                    "Quantity": len(value.get("custom_headers", {})),
                    "Items": [
                        {"HeaderName": ck, "HeaderValue": cv}
                        for ck, cv in value.get("custom_headers", {}).items()
                    ],
                },
            }
            for key, value in origins.items()
        ],
    }
    distribution_config["DefaultCacheBehavior"] = {
        "target_origin_id": target_origin,
        "TrustedSigners": {
            "Enabled": signed_urls,
            "Quantity": len(trusted_signers),
            "Items": trusted_signers,
        },
    }

    status, ret = await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="create_distribution",
        distribution_config=distribution_config,
        **kwargs,
    )
    await hub.exec.aws.cloud_front.distribution.tag(
        ctx, name, tags={ctx.acct.provider_tag_key: name}
    )
    return status, ret


async def delete(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="delete_distribution",
        name=name,
        **kwargs,
    )


async def get(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloud_front",
        func="get_distribution",
        name=name,
        **kwargs,
    )
    # Alternate method
    status, ret = await hub.aws.cloud_front.distribution.list()
    return status, ret.get(name)


async def list_(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    ret = []
    status, distribution = await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="list_distributions",
        **kwargs,
    )
    if not status:
        return status, distribution

    for distribution in distribution.get("TODO_ITEM_NAME", []):
        _, distribution.tags = await hub.exec.aws.cloud_front.distribution.tags(
            ctx, name=distribution.name
        )
        ret.append(distribution)
    return status, hub.tool.aws.dict.flatten_tags({"TODO_ITEMS": ret})


async def tag(
    hub, ctx, name: str, tags: Dict[str, str], **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="TODO_TAG_FUNC",
        name=name,
        tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        **kwargs,
    )


async def tags(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloud_front",
        func="TODO_GET_TAGS_FUNC",
        name=name,
        **kwargs,
    )


async def untag(hub, ctx, name: str, keys: List[str], **kwargs) -> Tuple[bool, Any]:
    return await hub.tool.aws.client.request(
        ctx,
        client="cloudfront",
        func="TODO_UNTAG_FUNC",
        name=name,
        tag_keys=keys,
        **kwargs,
    )


async def update(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    assert kwargs, "No keyword arguments were specified for updating"
    return await hub.tool.aws.client.request(
        ctx,
        client="cloud_front",
        func="TODO_UPDATE_FUNC",
        name=name,
        **kwargs,
    )
