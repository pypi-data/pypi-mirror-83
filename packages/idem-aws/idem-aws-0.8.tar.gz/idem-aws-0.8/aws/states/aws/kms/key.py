from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.kms.key.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted lambda key: {name}"}


async def present(
    hub,
    ctx,
    name: str,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    # Check if the key exists
    status, _ = await hub.exec.aws.kms.key.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.kms.key.create(
            ctx,
            name=name,
            **kwargs,
        )
        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created kms key: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
