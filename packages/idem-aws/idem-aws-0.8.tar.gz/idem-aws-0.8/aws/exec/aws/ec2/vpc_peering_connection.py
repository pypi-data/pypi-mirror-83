"""
EC2 VPC Peering Connection
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-vpc-peering-connections
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_vpc_peering_connections()
    return ret
