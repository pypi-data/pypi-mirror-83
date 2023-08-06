from typing import Any, Dict, List, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.dynamodb.table.delete(ctx, name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted dynamodb table: {name}"}


async def present(
    hub,
    ctx,
    name: str,
    attribute_definitions: List[Dict],
    key_schema: List[Dict],
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    status, table = await hub.exec.aws.dynamodb.table.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.dynamodb.table.create(
            ctx,
            name=name,
            attribute_definitions=attribute_definitions,
            key_schema=key_schema,
            **kwargs,
        )
        if not status:
            return False, {"comment": result.get("exception", result)}
        comments = [f"Created Dynamodb table: {name}"]

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
