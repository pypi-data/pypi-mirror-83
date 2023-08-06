from typing import Any, Dict, List, Tuple

# TODO Transparent requisites, I.E. All ec2 instances run after all keypairs have been created, networks set up,
#   and iam roles/permissions available
__treq__ = {}
# TODO have this happen before any bootstrapping states
__treq_in__ = {}


async def absent(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    status, result = await hub.exec.aws.ec2.instance.delete(ctx, name=name, **kwargs)
    if not status:
        return False, {"comment": result.get("exception", result)}

    return status, {"comment": f"Deleted ec2 instance: {name}"}


async def present(
    hub,
    ctx,
    name: str,
    subnet: str,
    deploy: bool = False,
    bootstrap_plugins: List[str] = None,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    if bootstrap_plugins is None:
        bootstrap_plugins = []
    status, instance = await hub.exec.aws.ec2.instance.get(ctx, name)
    comments = []

    if not status:
        status, result = await hub.exec.aws.ec2.instance.create(
            ctx, name=name, subnet=subnet, **kwargs
        )

        if not status:
            return False, {"comment": result.get("exception", result)}
        comments.append(f"Created Ec2 instance: {name}")

    if deploy:
        for plugin in bootstrap_plugins:
            deploy_ret = await getattr(hub.states.bootstrap, plugin).run(
                instance.user, ip_address=instance.NetworkInterfaces[0].PrivateIPAddress
            )
            comments.append(deploy_ret["comment"])
            # TODO use this for bootstrapping to send the master's public key temporarily:
            #   https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.send_ssh_public_key

    # TODO perform other updates as necessary
    if kwargs["vpcs"] != instance["vpcs"]:
        await hub.exec.aws.ec2.instance.update(
            ctx, func="attach_vpc", vpc=kwargs["vpc"]
        )

    return status, {"comment": "\n".join(comments)}
