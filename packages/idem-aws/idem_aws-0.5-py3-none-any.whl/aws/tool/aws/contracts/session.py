from dict_tools import data


def call_get(hub, ctx):
    new_ctx = data.NamespaceDict()

    # These are extra provider details that won't be passed to the session creation
    new_ctx.provider_tag_key = ctx.kwargs.pop("provider_tag_key", "Name")
    new_ctx.endpoint_url = ctx.kwargs.get("endpoint_url")

    kwargs = ctx.get_arguments()["kwargs"]
    aws_access_key_id = kwargs.pop("aws_access_key_id", None) or kwargs.pop("id", None)
    aws_secret_access_key = kwargs.pop("aws_secret_access_key", None) or kwargs.pop(
        "key", None
    )
    aws_session_token = kwargs.pop("aws_session_token", None) or kwargs.pop(
        "token", None
    )
    region_name = (
        kwargs.pop("region_name", None)
        or kwargs.pop("region", None)
        or kwargs.pop("location", None)
    )
    profile_name = kwargs.pop("profile_name", None) or kwargs.pop("profile", None)

    new_ctx.session = ctx.func(
        hub,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
        profile_name=profile_name,
        **kwargs,
    )

    return new_ctx
