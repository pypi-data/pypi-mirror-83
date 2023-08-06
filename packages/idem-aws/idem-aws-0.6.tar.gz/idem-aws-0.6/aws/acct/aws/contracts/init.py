from typing import Any, Dict


def sig_gather(hub) -> Dict[str, Any]:
    ...


async def post_gather(hub, ctx) -> Dict[str, Any]:
    """
    Sanitize these profiles and make sure they have everything needed
    """
    profiles = ctx.ret or {}

    hub.log.info(f"Read {len(profiles)} profiles from {ctx.ref}")

    # Check for existing profiles to warn about acct plugins that interfere with each other
    existing_profiles = hub.acct.aws.init.profiles()

    for profile in profiles:
        if profile in existing_profiles:
            hub.log.critical(
                f'Existing profile "{profile}" is being overwritten by {ctx.ref}'
            )

    return profiles
