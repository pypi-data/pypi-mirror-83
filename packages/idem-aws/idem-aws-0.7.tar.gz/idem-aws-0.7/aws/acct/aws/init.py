import configparser
import os
from typing import Set

# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_CONFIG_FILE = os.environ.get(
    "AWS_CONFIG_FILE",
    os.path.expanduser(os.path.join(os.path.expanduser("~"), ".aws", "config")),
)
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")
AWS_PROFILE = os.environ.get("AWS_PROFILE", "default")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SHARED_CREDENTIALS_FILE = os.environ.get(
    "AWS_SHARED_CREDENTIALS_FILE",
    os.path.join(os.path.expanduser("~"), ".aws", "credentials"),
)


def __virtual__(hub):
    return os.path.exists(AWS_SHARED_CREDENTIALS_FILE), "No existing aws configuration"


def __init__(hub):
    # Unlock acct by default if the virtual passed
    # This allows idem-aws to work with aws-cli configurations
    hub.acct.UNLOCKED = True


def profiles(hub) -> Set[str]:
    aws_profiles = set()
    for k, v in hub.acct.PROFILES.items():
        if k.startswith("aws"):
            aws_profiles.update(v.keys())
    return aws_profiles


async def gather(hub):
    """
    Get profile names from unencrypted existing AWS credential files
    """
    sub_profiles = {}
    config = configparser.ConfigParser()

    credential_files = [AWS_SHARED_CREDENTIALS_FILE]

    hub.log.info("Using unencrypted existing AWS credentials")
    config.read(credential_files)

    existing_profiles = hub.acct.aws.init.profiles()

    for profile in set(config.sections()):
        # Let boto do it's magic to figure out all the profile stuff based on the name

        if profile not in existing_profiles:
            sub_profiles[profile] = hub.tool.aws.session.get(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_session_token=AWS_SESSION_TOKEN,
                region_name=AWS_DEFAULT_REGION,
                profile_name=profile,
            )

    existing_profiles = hub.acct.aws.init.profiles()

    # Set the default idem-aws profile to the one defined in the environment
    if "default" not in existing_profiles:
        sub_profiles["default"] = hub.tool.aws.session.get(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_DEFAULT_REGION,
            profile_name=AWS_PROFILE,
        )

    return sub_profiles
