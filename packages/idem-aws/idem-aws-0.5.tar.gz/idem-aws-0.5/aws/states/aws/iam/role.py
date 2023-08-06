from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.iam.role.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted iam role: {name}"}


async def present(
    hub, ctx, name: str, assume_role_policy_document: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    # Check if the Role exists
    status, _ = await hub.exec.aws.iam.role.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.iam.role.create(
            ctx,
            name=name,
            assume_role_policy_document=assume_role_policy_document,
            **kwargs,
        )
        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created IAM Role: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
