"""
If a state fails for any reason then give a detailed error report in the return
"""
import asyncio
import traceback


async def call(hub, ctx):
    try:
        ret = ctx.func(*ctx.args, **ctx.kwargs)
        if asyncio.iscoroutine(ret):
            ret = await ret
        return ret
    except Exception as e:
        parent_ctx = ctx[1][1]
        kwargs = parent_ctx.get_arguments()
        return {
            "name": kwargs.get("name"),
            "result": False,
            "changes": {},
            "comment": "".join(
                traceback.format_exception(e.__class__, e, e.__traceback__)
            ).strip(),
        }
