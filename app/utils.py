import subprocess
import sh
from sh import bash

import re


def get_aliases():

    aliases = {}
    for alias in bash("-i", "-c", "alias", _iter=True):
        res = re.match('alias (.+)=\'(.+)\'', alias)
        if res:
            aliases[res.group(1)] = res.group(2)
    return aliases



