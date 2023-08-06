from typing import Any, Dict, Tuple
from dict_tools import data
import copy


def sig(hub, ctx, *args, **kwargs) -> Tuple[bool, Any]:
    ...


def pre(hub, ctx):
    func_ctx = ctx.kwargs.get("ctx", None)
    if func_ctx:
        if not func_ctx["acct"]:
            raise ValueError("missing account information")
        elif not func_ctx["acct"].get("session"):
            raise ValueError("Incomplete acct information: could not load session")


"""
TODO enforce these once we are further along
def sig_list(hub, ctx, **kwargs) -> Tuple[bool, List[Dict[str, Any]]]:
    ...


def sig_create(hub, ctx, name: str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    ...


def sig_delete(hub, ctx, name:str, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    ...


def sig_tag(hub, ctx, name:str, tags:Dict[str, str], **kwargs) -> Tuple[bool, Dict[str, Any]]:
    ...


def sig_tags(hub, ctx, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    ...
"""


# TODO Verify that another object with the same name tag doesn't already exist
async def pre_create(hub, ctx):
    ...


def post(hub, ctx):
    """
    in every function, only return the status if a state is asking
    """
    func_ctx = ctx.args[1]
    status, ret = ctx.ret
    if "run_name" in func_ctx:
        # If this is a state run then return the status of the call, otherwise, just return data
        return status, ret
    else:
        # If this was just an exec module then ignore the status
        return ret


async def post_list(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    Turn the output of list functions into a dictionary
    """
    func_ctx = ctx.args[1]
    status, result = ctx.ret

    if len(result) > 1:
        return status, result

    items: list = tuple(result.values())[0]

    # Re-arrange the list so that the keys come from the name tag
    if isinstance(items, dict):
        # The data has already been sanitized if it's in this format, carry on
        ret = items
    else:
        # Sanitize the data, ignore anything that isn't tagged with the provider tag key
        ret = data.NamespaceDict()
        for item in items:
            name = item.get("tags", {}).get(func_ctx["acct"].provider_tag_key)
            if name:
                if name in ret:
                    hub.log.error(f"Duplicate Name tags detected: {name}")
                    # Come up with an alternate name for listing the duplicate
                    j = 1
                    new_name = f"{name} ({j})"
                    while new_name in ret:
                        j += 1
                        new_name = f"{name} ({j})"
                    ret[new_name] = item
                else:
                    ret[name] = item

    # TODO is this how filters are meant to be applied?
    # Filter out data based on filters from OPT
    # don't filter if a state is asking
    if hub.OPT.idem.filter and "run_name" not in func_ctx:
        new_ret = data.NamespaceDict()
        for key, value in ret.items():
            new_ret[key] = data.NamespaceDict()
            for k, v in value.items():
                if k in hub.OPT.idem.filter:
                    new_ret[key][k] = v
        ret = new_ret
    return status, ret


def post_get(hub, ctx):
    status, ret = ctx.ret
    if isinstance(ret, dict):
        new_ret = data.NamespaceDict()
        for k, v in ret.items():
            # Only return values that are deep copyable
            try:
                new_ret[k] = copy.deepcopy(v)
            except (NotImplementedError, TypeError):
                pass
        ret = new_ret
    return status, ret


def post_tags(hub, ctx):
    status, ret = ctx.ret
    if not status:
        return ctx.ret
    tags = tuple(ret.values())[0]
    if isinstance(tags, dict):
        return status, tags
    else:
        return status, {tag.key: tag.value for tag in tags}
