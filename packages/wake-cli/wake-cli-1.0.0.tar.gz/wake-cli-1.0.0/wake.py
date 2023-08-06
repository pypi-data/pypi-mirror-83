#!/Users/james/.local/share/virtualenvs/Wake-pFO7HIXT/bin/python
"""
Wake brings together your ssh config and WakeOnLan together,
so you can use the same aliases you use to ssh to your machines,
to wake them up.

Usage:
  wake <alias>
  wake -h | --help
  wake --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
import os
import re
import sys
import enum

import docopt
import paramiko
import wakeonlan


VERSION = (1, 0, 0)
__version__ = ".".join(map(str, VERSION))

SSH_CONFIG_PATH = os.path.expanduser("~/.ssh/config")
MAC_ADDRESS_PATTERN = re.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")

TERM_COLOR_RED = "\u001b[31m"
TERM_COLOR_RESET = "\u001b[0m"


class ExitCode(enum.Enum):
    SUCCESS = 0
    SSH_CONFIG_NOT_FOUND = 1
    MAC_ADDRESS_NOT_FOUND = 2


def stderr(msg):
    print(TERM_COLOR_RED + msg + TERM_COLOR_RESET, file=sys.stderr)


def wake(alias):
    if MAC_ADDRESS_PATTERN.match(alias):
        mac_address = alias
    else:
        try:
            with open(SSH_CONFIG_PATH) as fp:
                ssh_config = paramiko.SSHConfig.from_file(fp)
        except FileNotFoundError:
            stderr(f'No ssh config file found at "{SSH_CONFIG_PATH}"')
            exit(ExitCode.SSH_CONFIG_NOT_FOUND.value)

        host_config = ssh_config.lookup(alias)

        try:
            mac_address = host_config["macaddress"]
        except KeyError:
            stderr(f'No macaddress found for alias {alias} in "{SSH_CONFIG_PATH}"')
            exit(ExitCode.MAC_ADDRESS_NOT_FOUND.value)

    wakeonlan.send_magic_packet(mac_address)

    if alias == mac_address:
        print(f"Magic packet sent to {alias}")
    else:
        print(f"Magic packet sent to {alias} ({mac_address})")

    exit(ExitCode.SUCCESS.value)


def cli():
    arguments = docopt.docopt(__doc__, version=VERSION, help=True)
    wake(arguments["<alias>"])


if __name__ == '__main__':
    cli()
