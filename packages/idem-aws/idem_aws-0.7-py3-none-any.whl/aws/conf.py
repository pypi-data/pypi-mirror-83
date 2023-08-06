CLI_CONFIG = {
    "filter": {
        "options": ["--filter"],
        "nargs": "*",
    },
    "session_backend": {
        "options": ["--session-backend"],
        "choices": ["aioboto3", "boto3", "localstack"],
    },
    "wrap_serial_calls": {
        "options": ["--wrap-serial-calls"],
        "action": "store_true",
    },
}
CONFIG = {
    # TODO will this option apply more broadly to idem-cloud?
    "filter": {
        "help": "Filters to apply to all lists from AWS",
        "dyne": "idem",
        "subcommands": ["exec"],
        "default": None,
        "os": "IDEM_AWS_LIST_FILTERS",
    },
    "session_backend": {
        "help": "Specify the boto session backend plugin to use",
        "dyne": "idem",
        "subcommands": ["exec", "state"],
        "default": None,
        "type": str,
        "os": "IDEM_AWS_SESSION_BACKEND",
    },
    "wrap_serial_calls": {
        "help": "Wrap serial calls to make them async",
        "dyne": "idem",
        "subcommands": ["state"],
        "default": False,
        "type": bool,
        "os": "IDEM_AWS_WRAP_SERIAL_CALLS",
    },
}
SUBCOMMANDS = {}
DYNE = {
    "acct": ["acct"],
    "exec": ["exec"],
    "states": ["states"],
    "tool": ["tool"],
}
