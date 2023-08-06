from dict_tools import data


async def pre_get(hub, ctx):
    kwargs = ctx.get_arguments()
    func_ctx = kwargs["ctx"]
    if not func_ctx.get("acct"):
        raise ConnectionError("missing acct profile")
    elif not func_ctx["acct"].get("session"):
        raise ConnectionError("Incomplete profile information: missing session")


def sig_request(hub, ctx, client: str, func: str, **kwargs):
    ...


def pre_request(hub, ctx):
    """
    Verify that the ctx has all the information it needs from the profile
    """
    kwargs = ctx.get_arguments()
    func_ctx = kwargs["ctx"]
    if not func_ctx.get("acct"):
        raise ConnectionError("missing acct profile")
    elif not func_ctx["acct"].get("session"):
        raise ConnectionError("Incomplete profile information: missing session")


async def call_request(hub, ctx):
    kwargs = ctx.get_arguments()
    # See if "Dromedary case" was set (first character is lowercase)
    dromedary = kwargs["kwargs"].pop("dromedary", False)
    camel = hub.tool.aws.dict.camelize(kwargs["kwargs"], dromedary)
    try:
        return await ctx.func(
            hub, kwargs["ctx"], client=kwargs["client"], func=kwargs["func"], **camel
        )
    except Exception as e:
        return data.NamespaceDict({"exception": str(e), "http_status_code": None})


def _http_success(ctx, response: data.NamespaceDict) -> bool:
    kwargs = ctx.get_arguments()
    if kwargs["client"] == "s3" and "delete" in kwargs["func"]:
        # Boto's S3 delete_bucket returns the wrong status code: https://github.com/boto/boto3/issues/759
        return response.get("http_status_code", None) in (200, 204)

    return response.get("http_status_code", None) == 200


def post_request(hub, ctx):
    ret = ctx.ret
    if isinstance(ret, dict):
        ret = hub.tool.aws.dict.de_camelize(ret)
        ret = hub.tool.aws.dict.flatten_tags(ret)
        response = ret.pop("response_metadata", {})
        return _http_success(ctx, response), ret
    return None, ret
