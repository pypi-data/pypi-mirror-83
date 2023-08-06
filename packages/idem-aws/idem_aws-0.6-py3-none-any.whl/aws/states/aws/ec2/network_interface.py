from typing import Any, Dict, Tuple


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.ec2.network_interface.delete(
        ctx, name=name, **kwargs
    )
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted ec2 network_interface: {name}"}


async def present(
    hub, ctx, name: str, subnet: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    status, network_interface = await hub.exec.aws.ec2.network_interface.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.ec2.network_interface.create(
            ctx, name=name, subnet=subnet, **kwargs
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created Ec2 network interface: {name}")

    # TODO perform other updates as necessary

    return status, {"comment": "\n".join(comments)}
