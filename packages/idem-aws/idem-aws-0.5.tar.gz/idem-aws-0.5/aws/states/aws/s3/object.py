from typing import Any, Dict, Tuple


async def absent(
    hub, ctx, name: str, bucket: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.s3.object.delete(
        ctx, name=name, bucket=bucket, **kwargs
    )
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted s3 object: {name}"}


async def present(
    hub, ctx, name: str, bucket: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    # Check if the object exists
    status, _ = await hub.exec.aws.s3.object.get(ctx, name, bucket=bucket)
    comments = []

    if not status:
        # The s3 object doesn't exist, create it
        status, result = await hub.exec.aws.s3.object.create(
            ctx,
            name=name,
            bucket=bucket,
            **kwargs,
        )
        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created S3 Object: {name}")

    return status, {"comment": "\n".join(comments)}
