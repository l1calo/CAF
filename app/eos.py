import utils
import sh
import logging
logger = logging.getLogger(__name__)


def cmd():
    eos_cmd = utils.get_aliases().get('eos', None)
    if eos_cmd:
        return sh.Command(eos_cmd)

EOS_CMD = cmd()

if not EOS_CMD:
    raise Exception("Could not find eos command")


def ls(folder):
    try:
        res = EOS_CMD.ls(folder)
        return res
    except:
        return None
