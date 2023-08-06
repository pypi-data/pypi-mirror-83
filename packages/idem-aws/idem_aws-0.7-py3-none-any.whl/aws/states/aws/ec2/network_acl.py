from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.ec2.network_acl.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted ec2 network_acl: {name}"}


async def present(
    hub, ctx, name: str, vpc: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, network_acl = await hub.exec.aws.ec2.network_acl.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.ec2.network_acl.create(
            ctx, name=name, vpc=vpc, **kwargs
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created Ec2 network acl: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
