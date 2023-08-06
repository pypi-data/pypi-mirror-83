from dict_tools import data, differ
from typing import Dict, Tuple

AWS_OBJECT_NAME = lambda ctx: " ".join(ctx.ref.split(".")).title()


def sig(hub, ctx, name: str, *args, **kwargs) -> Tuple[bool, Dict[str, str]]:
    ...


def pre(hub, ctx):
    func_ctx = ctx.kwargs.get("ctx", None)
    if func_ctx:
        if not func_ctx["acct"]:
            raise ValueError("missing account information")
        elif not func_ctx["acct"].get("session"):
            raise ValueError("Incomplete acct information: could not load session")


async def call_absent(hub, ctx):
    kwargs = ctx.get_arguments()

    ret = data.NamespaceDict(
        name=kwargs["name"],
        result=False,
        changes=None,
        comment="",
    )
    # Find the "get item" function for this sub
    get_func = hub.exec.aws
    for ref in f"{ctx.ref}.get".split("."):
        get_func = getattr(get_func, ref)
    # if the get_func has some of the same kwargs as the called func then pass them through
    get_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k in get_func.signature.parameters and k not in ("hub", "ctx", "name")
    }
    get_kwargs.update(get_kwargs.pop("kwargs", {}))

    ret.result, changes_old = await get_func(
        kwargs["ctx"], kwargs["name"], **get_kwargs
    )

    if not ret.result:
        ret.comment = f"{AWS_OBJECT_NAME(ctx)} `{kwargs['name']}` is already absent"
        return ret

    ret.result, result = await ctx.func(*ctx.args, **ctx.kwargs)

    if not ret.result:
        ret.comment = result.get("exception", result)
    else:
        ret.comment = f"{AWS_OBJECT_NAME(ctx)} `{kwargs['name']}` was deleted"

    # If the state had a uniquely defined result add it here
    ret.update(result)

    _, changes_new = await get_func(kwargs["ctx"], kwargs["name"], **get_kwargs)
    ret.changes = differ.deep_diff(changes_old, changes_new)

    return ret


async def call_present(hub, ctx):
    kwargs = ctx.get_arguments()

    ret = data.NamespaceDict(
        name=kwargs["name"],
        result=False,
        changes=None,
        comment="",
    )

    # Find the "get item" function for this sub
    sub = hub.exec.aws
    for ref in ctx.ref.split("."):
        sub = getattr(sub, ref)

    # Find some common functions that should be available for every state
    get_func = getattr(sub, "get")
    tag_func = getattr(sub, "tag", None)
    tags_func = getattr(sub, "tags", None)
    untag_func = getattr(sub, "untag", None)

    # if the get_func has some of the same kwargs as the called func then pass them through
    get_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k in get_func.signature.parameters and k not in ("hub", "ctx", "name")
    }
    get_kwargs.update(get_kwargs.pop("kwargs", {}))
    ret.result, changes_old = await get_func(
        kwargs["ctx"], kwargs["name"], **get_kwargs
    )

    # tagging will be handled a different way
    tags = kwargs.pop("tags", {})
    kwargs.update(kwargs.pop("kwargs", {}))

    # Call the actual "present" function
    ret.result, result = await ctx.func(**kwargs)

    if not ret.result:
        return ret

    # Go into the whole tagging routine if the tagging functions exist
    if tag_func and tags_func and untag_func and tags:
        tag_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k in tag_func.signature.parameters
            and k in tags_func.signature.parameters
            and k in untag_func.signature.parameters
            and k not in ("hub", "ctx", "name")
        }
        old_tags_status, old_tags = await tags_func(
            kwargs["ctx"], kwargs["name"], **tag_kwargs
        )

        # Make sure the main name tag is correct
        if old_tags.get(kwargs["ctx"].acct.provider_tag_key) != kwargs["name"]:
            status, _ = await tag_func(
                kwargs["ctx"],
                kwargs["name"],
                tags={kwargs["ctx"].acct.provider_tag_key: kwargs["name"]},
                **tag_kwargs,
            )
            ret.result = ret.result and status

        # If the tags are None then don't change any other tags
        if tags is not None:
            if old_tags_status:
                tag_diff = differ.diff(old_tags, tags)
            else:
                tag_diff = differ.diff({}, tags)
            for key in tag_diff.added():
                ret.comment += f"\nadded tags: {', '.join(tag_diff.added())}"
                status, _ = await tag_func(
                    kwargs["ctx"],
                    kwargs["name"],
                    tags={key: old_tags[key]},
                    **tag_kwargs,
                )
                ret.result = ret.result and status
            if tag_diff.removed():
                ret.comment += f"\nremoved tags: {', '.join(tag_diff.removed())}"
                status, _ = await untag_func(
                    kwargs["ctx"],
                    kwargs["name"],
                    keys=tag_diff.removed(),
                    **tag_kwargs,
                )
                ret.result = ret.result and status

    # If the state had a uniquely defined result add it here
    ret.update(result)

    # Report the changes the same way for every single state
    _, changes_new = await get_func(kwargs["ctx"], kwargs["name"], **get_kwargs)
    ret.changes = differ.deep_diff(changes_old, changes_new)

    return ret
