from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.ec2.security_group.delete(
        ctx, name=name, **kwargs
    )
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted ec2 security_group: {name}"}


async def present(
    hub, ctx, name: str, description: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, security_group = await hub.exec.aws.ec2.security_group.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.ec2.security_group.create(
            ctx, name=name, description=description, **kwargs
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created Ec2 security_group: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
