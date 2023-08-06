from typing import Any, Dict


def sig_get(
    hub,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    aws_session_token: str = None,
    region_name: str = None,
    profile_name: str = None,
    **kwargs,
) -> Dict[str, Any]:
    ...
