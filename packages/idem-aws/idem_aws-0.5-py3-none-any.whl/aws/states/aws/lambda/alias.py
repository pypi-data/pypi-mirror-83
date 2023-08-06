from typing import Any, Dict, Tuple


async def absent(
    hub, ctx, name: str, function_name: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.λ.alias.delete(
        ctx, name=name, function_name=function_name, **kwargs
    )
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted lambda alias: {name}"}


async def present(
    hub,
    ctx,
    name: str,
    function_name: str,
    function_version: str,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    # Check if the alias exists
    status, _ = await hub.exec.aws.λ.alias.get(ctx, name, function_name=function_name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.λ.alias.create(
            ctx,
            name=name,
            function_name=function_name,
            function_version=function_version,
            **kwargs,
        )
        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created lambda alias: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
