from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.λ.function.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted lambda function: {name}"}


async def present(
    hub,
    ctx,
    name: str,
    runtime: str,
    role: str,
    handler: str,
    code: Dict[str, str],
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    # Check if the function exists
    status, _ = await hub.exec.aws.λ.function.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.λ.function.create(
            ctx,
            name=name,
            runtime=runtime,
            role=role,
            handler=handler,
            code=code,
            **kwargs,
        )
        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created lambda function: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
