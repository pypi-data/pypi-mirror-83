from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.ec2.snapshot.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted ec2 snapshot: {name}"}


async def present(
    hub, ctx, name: str, volume: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, snapshot = await hub.exec.aws.ec2.snapshot.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.ec2.snapshot.create(
            ctx, name=name, volume=volume, **kwargs
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created Ec2 snapshot: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
