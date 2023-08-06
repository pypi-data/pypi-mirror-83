from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.ec2.image.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted ec2 image: {name}"}


async def present(
    hub, ctx, name: str, instance: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, image = await hub.exec.aws.ec2.image.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.ec2.image.create(
            ctx, name=name, instance=instance, **kwargs
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created Ec2 image: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
