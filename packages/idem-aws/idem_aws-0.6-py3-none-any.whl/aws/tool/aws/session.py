import os
import sys


def get(hub, *args, **kwargs):
    # Get the default session from environment variables, this is normally handled by conf.py,
    # But for pytest we also need to specify it here.
    # If the environment variable isn't set and we are running in pytest, default to localstack, else aioboto3
    env_default = os.environ.get(
        "IDEM_AWS_SESSION_BACKEND",
        "localstack" if "pytest" in sys.modules else "aioboto3",
    )

    backends = hub.tool.aws.backend._loaded.keys()
    default = env_default if env_default in backends else next(iter(backends))

    # Use the specified session backend
    # if it doesn't exist, fall back on the default if it is loaded
    # if the default isn't loaded then use the first loaded session backend
    session_backend = hub.OPT.idem.session_backend or default
    if session_backend not in backends:
        raise ConnectionError(f"Backend not loaded: {session_backend}")
    return getattr(hub.tool.aws.backend, session_backend).get(*args, **kwargs)
