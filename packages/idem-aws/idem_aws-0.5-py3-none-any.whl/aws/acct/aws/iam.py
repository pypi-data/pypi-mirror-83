import configparser
import logging
import os

log = logging.getLogger(__name__)

"""
https://blog.gruntwork.io/authenticating-to-aws-with-the-credentials-file-d16c0fbcbf9e

$ aws configure
AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json

AWS prompts you to enter your Access Key ID and Secret Access Key and stores them in ~/.aws/credentials:

[default]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

It also stores the other settings you entered in ~/.aws/config:

[default]
region=us-west-2
output=json
"""


async def gather(hub):
    """
    Get profile names from unencrypted AWS credential files

    Example:
    .. code-block:: yaml

        aws.iam:
            - ~/.aws/credentials
            - /path/to/other/credential/file
    """
    default_cred_file = os.path.expanduser("~/.aws/credentials")
    sub_profiles = {}
    config = configparser.ConfigParser()

    credential_files = hub.acct.PROFILES.get("aws.iam", [])

    # If no other credential files were defined then grab the default
    if not credential_files and os.path.exists(default_cred_file):
        log.warning("Reading unencrypted default aws credential file")
        credential_files.append(default_cred_file)

    config.read(credential_files)

    if config.sections():
        log.warning("Gathering unencrypted credentials from file system.")

    # Check for existing profiles that might be overwritten by unencrypted credentials
    aws_profiles = set()
    for k, v in hub.acct.PROFILES.items():
        if k.startswith("aws"):
            aws_profiles.update(v.keys())

    for profile in set(config.sections()):
        if profile in aws_profiles:
            log.debug(
                f"Profile '{profile}' already exists, not overwriting with unencrypted creds"
            )
            continue
        # Let boto do it's magic to figure out all the profile stuff based on the name
        sub_profiles[profile] = hub.tool.aws.session.get(profile_name=profile)

    return sub_profiles
