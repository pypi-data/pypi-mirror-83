from typing import Any, Dict, List, Tuple


async def vpc_resource(
    hub,
    ctx,
    subnets: List[str] = None,
    security_groups: List[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Create a VPC resource config, add extra kwargs to config
    """
    result = kwargs.copy()
    result["subnet_ids"] = []
    for subnet in subnets or ():
        status, subnet = await hub.exec.aws.ec2.subnet.get(ctx, subnet)
        if not status:
            return {}
        result["subnet_ids"].append(subnet.subnet_id)

    result["security_group_ids"] = []
    for security_group in security_groups or ():
        status, security_group = await hub.exec.aws.ec2.security_group.get(
            ctx, security_group
        )
        if not status:
            return {}
        result["security_group_ids"].append(security_group.group_id)

    return result


def scaling(
    hub, ctx, min_size: int = None, max_size: int = None, desired_size: int = None
) -> Dict[str, int]:
    """
    Create a scalingConfig, discard all extra kwargs
    """
    if not min_size and not max_size and not desired_size:
        return

    assert min_size > 0
    return {
        "min_size": int(min_size),
        "max_size": int(max_size),
        "desired_size": int(desired_size),
    }
