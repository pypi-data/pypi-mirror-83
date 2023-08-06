from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.eks.nodegroup.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted eks nodegroup: {name}"}


async def present(
    hub, ctx, name: str, cluster: str, tags: Dict[str, str] = None, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create the named AWS resource if it doesn't exist.
    Verify that the tags on the resource are as specified in the tags argument and ctx.
    The results dictionary as well as tagging are handled in the global states contract:
        - idem_aws/states/aws/contracts/init.py:call_present

    :param name: The name of the resource to manage
    :param tags: The tags to manage on the resource
        - Extra tags will be added to the resource
        - Missing tags will be removed from the resource
        - The ctx.provider_tag_key will be automatically added to the tags
    :param kwargs: Any keyword arguments to pass to the sub's 'update' function
    """
    # Check if the nodegroup exists
    status, _ = await hub.exec.aws.eks.nodegroup.get(ctx, name)
    comments = []

    if not status:
        # The eks nodegroup doesn't exist, create it
        status, result = await hub.exec.aws.eks.nodegroup.create(
            ctx, name, cluster, **kwargs
        )
        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created eks nodegroup: {name}")

    if kwargs:
        # TODO determine if updating is necessary, maybe by getting the revision_id from nodegroup?
        new_status, _ = await hub.exec.aws.eks.nodegroup.update(ctx, name, **kwargs)

    return status, {"comment": "\n".join(comments)}
