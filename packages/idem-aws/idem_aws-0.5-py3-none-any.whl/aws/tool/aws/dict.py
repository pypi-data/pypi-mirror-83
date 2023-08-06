"""
This is where utils for the entire idem-aws plugin belong
"""
import re
from dict_tools import data
from typing import Any, Dict, Match


def __init__(hub):
    hub.tool.aws.RE_CAMEL = re.compile("([A-Z]*)([A-Z][a-z0-9]+)")


def _camel_sub(match: Match) -> str:
    ret = match.group(1).lower()
    if ret:
        ret += "_"
    return ret + match.group(2).lower() + "_"


def de_camelize(hub, kwargs: [Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(kwargs, dict):
        return kwargs

    ret = data.NamespaceDict()
    for key, value in kwargs.items():
        decameled_key = (
            hub.tool.aws.RE_CAMEL.sub(_camel_sub, key).strip("_").replace("-", "_")
        )
        if isinstance(value, dict):
            ret[decameled_key] = hub.tool.aws.dict.de_camelize(value)
        elif isinstance(value, list):
            ret[decameled_key] = [
                hub.tool.aws.dict.de_camelize(v) if isinstance(v, dict) else v
                for v in value
            ]
        else:
            ret[decameled_key] = value
    return ret


def camel(hub, item: str, dromedary: bool = False) -> str:
    if "_" not in item and (dromedary or item[0].isupper()):
        # Already cameled
        return item
    else:
        # Replace underscores with spaces then call str()'s tile() method, then get rid of spaces
        result = item.replace("_", " ").title().replace(" ", "")
        if dromedary:
            return result[0].swapcase() + result[1:]
        return result


def camelize(hub, kwargs: Dict[str, Any], dromedary: bool = False) -> Dict[str, Any]:
    """Return a dictionary that can be :**:'d or merged into the arguments
    to a function - boto3's arguments are all CamelCased to go along
    with the AWS API's conventions.

    This changes any known key in the
    kwargs, which would be snake_cased per the conventions in
    salt/idem/pop, into being their corresponding camel-cased
    equivalents.

    Values of None will be filtered out since None isn't helpful when
    passing it into the API (it breaks things)

    An example map from EBS volume resources follows:
    # Map of properties that the AWS API has in camel case, vs. the
    # snake case that is provided via salt/pop/idem
    CAMEL_MAP = {
        'availability_zone': 'AvailabilityZone',
        'encrypted': 'Encrypted',
        'iops': 'Iops',
        'kms_key_id': 'KmsKeyId',
        'size': 'Size',
        'snapshot_id': 'SnapshotId',
        'volume_type': 'VolumeType',
        'dry_run': 'DryRun',
        'tag_specifications': 'TagSpecifications',
        'resource_type': 'ResourceType', # For tag
        'tags': 'Tags',  # for tag
        'filters': 'Filters',
        'multi_attach_enabled': 'MultiAttachEnabled'
    }

    If the "dromedary" flag is set, the first character will be lowercased
    """
    return {
        hub.tool.aws.dict.camel(k, dromedary): v
        for k, v in kwargs.items()
        # Skip key/value pairs that are None, they break things in boto3
        if v is not None
    }


def flatten_tags(hub, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    ret = data.NamespaceDict()
    for key, value in kwargs.items():
        if key.lower() == "tags":
            if isinstance(value, list):
                ret[key] = {
                    v.get("key", v.get("tag_key")): v.get("value", v.get("tag_value"))
                    for v in value
                }
            else:
                ret[key] = value
        elif isinstance(value, dict):
            ret[key] = hub.tool.aws.dict.flatten_tags(value)
        elif isinstance(value, list):
            ret[key] = [
                hub.tool.aws.dict.flatten_tags(v) if isinstance(v, dict) else v
                for v in value
            ]
        else:
            ret[key] = value
    return ret
