from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.s3.bucket.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted s3 bucket: {name}"}


async def present(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, _ = await hub.exec.aws.s3.bucket.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.s3.bucket.create(
            ctx,
            name=name,
            **kwargs,
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created s3 bucket: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
