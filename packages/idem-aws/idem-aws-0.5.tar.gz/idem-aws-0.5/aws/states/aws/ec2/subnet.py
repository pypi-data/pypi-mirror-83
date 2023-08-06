from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.ec2.subnet.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted ec2 subnet: {name}"}


async def present(
    hub, ctx, name: str, cidr_block: str, vpc: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, subnet = await hub.exec.aws.ec2.subnet.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.ec2.subnet.create(
            ctx, name=name, cidr_block=cidr_block, vpc=vpc, **kwargs
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created Ec2 subnet: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
