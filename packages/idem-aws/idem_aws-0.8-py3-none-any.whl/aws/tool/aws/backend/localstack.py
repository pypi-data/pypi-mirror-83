import os
import urllib.parse

try:
    import localstack_client.session

    HAS_LOCALSTACK = True
except ImportError as e:
    HAS_LOCALSTACK = False, str(e)


def __virtual__(hub):
    return HAS_LOCALSTACK


def __init__(hub):
    ...


# Stub that will get profile info out of the pop `acct` plugin.
def get(
    hub,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    aws_session_token: str = None,
    region_name: str = None,
    profile_name: str = None,
    **kwargs,
):
    endpoint_url = kwargs.get("endpoint_url", None)
    if endpoint_url:
        parsed = urllib.parse.urlparse(endpoint_url)
        localstack_host = parsed.hostname
        if parsed.scheme == "https":
            os.environ["USE_SSL"] = "true"

    else:
        localstack_host = None
    return localstack_client.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
        profile_name=profile_name,
        localstack_host=localstack_host,
    )
