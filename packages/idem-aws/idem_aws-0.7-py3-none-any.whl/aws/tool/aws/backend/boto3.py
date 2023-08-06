try:
    import boto3

    HAS_BOTO3 = True
except ImportError as e:
    HAS_BOTO3 = False, str(e)


def __virtual__(hub):
    return HAS_BOTO3


def __init__(hub):
    # Overwrite the boto3 logger so we don't see duplicate log messages
    boto3.set_stream_logger("", level=100)


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
    return boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
        profile_name=profile_name,
    )
