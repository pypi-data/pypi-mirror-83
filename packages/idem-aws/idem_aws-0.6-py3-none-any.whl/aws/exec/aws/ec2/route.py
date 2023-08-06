"""
EC2 Route
"""
from typing import Any, Dict, List, Tuple

__func_alias__ = {"list_": "list"}


async def create(
    hub,
    ctx,
    route_table: str,
    cidr_block: str = None,
    ipv6_cidr_block: str = None,
    prefix: str = None,
    **kwargs,
):
    """
    You must specify one of the following targets:
        - internet gateway or virtual private gateway
        - NAT instance
        - NAT gateway
        - VPC peering connection
        - network interface
        - egress-only internet gateway
        - transit gateway
    :param name:
    # TODO turn each of these named objects from kwargs into the appropriate ID
    :param cidr_block: Destination ipv4 cidr block
    :param ipv6_cidr_block: Destination ipv6 cidr block
    :param prefix: The ID of a prefix list used for the destination CIDR_BLOCK match
    :param route_table:
    :param kwargs: One of
            - destination_cidr_block
            - destination_ipv6_cidr_block
            - destination_prefix_list
            - egress_only_internet_gateway
            - gateway
            - instance
            - nat_gateway
            - transit_gateway
            - local_gateway
            - carrier_gatewayS
            - network_interface
            - vpc_peering_connection
    """
    assert cidr_block or ipv6_cidr_block, "Need an ipv4 or ipv6 cidr block"
    target_kwargs = {}
    for target, value in kwargs.items():
        if target == "gateway":
            _, result = await hub.exec.aws.ec2.gateway.get(ctx, value)
            target_kwargs["gateway_id"] = result.gateway_id
        elif target == "instance":
            _, result = await hub.exec.aws.ec2.instance.get(ctx, value)
            target_kwargs["instance_id"] = result.instance_id
        elif target == "nat_gateway":
            _, result = await hub.exec.aws.ec2.nat_gateway.get(ctx, value)
            target_kwargs["nat_gateway_id"] = result.nat_gateway_id
        elif target == "transit_gateway":
            _, result = await hub.exec.aws.ec2.transit_gateway.get(ctx, value)
            target_kwargs["transit_gateway_id"] = result.transit_gateway_id
        elif target == "local_gateway":
            _, result = await hub.exec.aws.ec2.local_gateway.get(ctx, value)
            target_kwargs["local_gateway_id"] = result.local_gateway_id
        elif target == "carrier_gateway":
            _, result = await hub.exec.aws.ec2.carrier_gateway.get(ctx, value)
            target_kwargs["carrier_gateway_id"] = result.carrier_gateway_id
        elif target == "network_interface":
            _, result = await hub.exec.aws.ec2.network_interface.get(ctx, value)
            target_kwargs["network_interface_id"] = result.network_interface_id
        elif target == "vpc_peering_connection":
            _, result = await hub.exec.aws.ec2.vpc_peering_connection.get(ctx, value)
            target_kwargs[
                "vpc_peering_connection_id"
            ] = result.vpc_peering_connection_id
        else:
            target_kwargs[target] = value

    _, route_table = await hub.exec.aws.ec2.route_table.get(ctx, route_table)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="create_route",
        route_table_id=route_table.route_table_id,
        destination_cidr_block=cidr_block,
        destination_ipv6_cidr_block=ipv6_cidr_block,
        # TODO turn this into an ID based on a name
        destination_prefix_list_id=prefix,
        dry_run=ctx.get("test", False),
        **target_kwargs,
    )


async def delete(
    hub,
    ctx,
    route_table: str,
    cidr_block: str = None,
    ipv6_cidr_block: str = None,
    prefix: str = None,
    **kwargs,
):
    _, route_table = await hub.exec.aws.ec2.route_table.get(ctx, route_table)
    return await hub.tool.aws.client.request(
        ctx,
        client="ec2",
        func="delete_route",
        destination_cidr_block=cidr_block,
        destination_ipv6_cidr_block=ipv6_cidr_block,
        # TODO turn this into an ID based on a name
        destination_prefix_list_id=prefix,
        route_table_id=route_table.route_table_id,
        dry_run=ctx.get("test", False),
        **kwargs,
    )


async def get(
    hub,
    ctx,
    cidr_block: str = None,
    ipv6_cidr_block: str = None,
    prefix: str = None,
):
    raise NotImplementedError("TODO")


async def list_(hub, ctx, route_table: str):
    status, route_table = await hub.exec.aws.ec2.route_table.get(ctx, route_table)
    return status, {"routs": route_table.routes}
