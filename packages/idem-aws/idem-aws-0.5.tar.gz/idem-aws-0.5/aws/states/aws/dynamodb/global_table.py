from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.dynamodb.global_table.delete(
        ctx, name, **kwargs
    )
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted dynamodb global_table: {name}"}


async def present(
    hub,
    ctx,
    name: str,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    status, global_table = await hub.exec.aws.dynamodb.global_table.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.dynamodb.global_table.create(
            ctx,
            name=name,
            **kwargs,
        )
        if not status:
            return False, {"comment": result.get("exception", result)}
        comments = [f"Created Dynamodb global table: {name}"]

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
