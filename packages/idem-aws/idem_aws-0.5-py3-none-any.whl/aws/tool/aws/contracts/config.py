import asyncio


async def call(hub, ctx):
    args = ctx.get_arguments()
    kwargs = args.pop("kwargs", {})
    dromedary = kwargs.pop("dromedary", False)

    ret = ctx.func(*[v for v in args.values()], **kwargs)
    if asyncio.iscoroutine(ret):
        ret = await ret

    return hub.tool.aws.dict.camelize(ret, dromedary)
