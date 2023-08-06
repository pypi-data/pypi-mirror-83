import argparse
import os
import subprocess
import sys
import traceback
from typing import List

from zuper_commons.logs import setup_logging
from zuper_commons.text.zc_wildcards import expand_wildcard

from . import logger
from .commons import get_dir_info

__all__ = ["aido_check_not_dirty_main"]


def aido_check_not_dirty_main(args=None):
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", default=".")
    parser.add_argument("cmd", nargs="*")
    parsed = parser.parse_args(args)
    try:
        directory = parsed.directory
        absdir = os.path.realpath(directory)
        rest = parsed.cmd

        if not os.path.exists(directory):
            sys.exit(-2)

        di = get_dir_info(directory)

        setup = os.path.join(absdir, "setup.py")
        if os.path.exists(setup):
            # if python package, we only care about python files
            allchanges = di.modified + di.deleted + di.untracked + di.added

            pyfiles = [_ for _ in allchanges if _.endswith(".py")]
            others = [_ for _ in allchanges if not _.endswith(".py")]
            py_dirty = len(pyfiles) > 0

            if not py_dirty and di.dirty:
                msg = "Python package detected. Ignoring non-python file changes."
                logger.info(msg, ignored=others)
            di.dirty = py_dirty
        else:
            allchanges = di.modified + di.deleted + di.untracked + di.added
            allchanges = remove_to_ignore(allchanges)
            logger.info(allchanges=allchanges)

            di.dirty = len(allchanges) > 0

        if di.dirty:
            logger.error("The directory is dirty.", directory=absdir, di=di, rest=" ".join(rest))
            sys.exit(1)

        else:
            # logger.info('This is not dirty.',
            #              directory=absdir, di=di, rest=" ".join(rest))
            if rest:
                res = subprocess.run(rest, cwd=directory)
                sys.exit(res.returncode)
            else:
                sys.exit(0)

    except SystemExit:
        raise
    except:
        logger.error(traceback.format_exc())
        sys.exit(3)


def remove_to_ignore(a: List[str]) -> List[str]:
    to_remove = ["*.resolved", ".gitignore"]
    for i in to_remove:
        try:
            no = expand_wildcard(i, a)
        except ValueError:
            no = []
        else:
            logger.info(f"ignoring {a} because {i}")
        a = [_ for _ in a if _ not in no]
    return a
