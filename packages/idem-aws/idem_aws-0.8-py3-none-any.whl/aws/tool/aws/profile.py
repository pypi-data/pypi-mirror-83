from typing import Set

__func_alias__ = {"list_": "list"}


def list_(hub) -> Set[str]:
    aws_profiles = set()
    for k, v in hub.acct.PROFILES.items():
        if k.startswith("aws"):
            aws_profiles.update(v.keys())
    return aws_profiles
