from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.ec2.volume.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted ec2 volume: {name}"}


async def present(
    hub, ctx, name: str, availability_zone: str, size: int, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, volume = await hub.exec.aws.ec2.volume.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.ec2.volume.create(
            ctx, name=name, availability_zone=availability_zone, size=size, **kwargs
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created Ec2 Volume: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
