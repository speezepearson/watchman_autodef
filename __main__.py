import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Sequence, Set, NewType

import watchman_autodef

AUTODEF_PREFIX = 'autodef.'
RELOADER_NAME = 'autodef-reload'

def update(args: Any) -> None:
    watchman_autodef.update(dir=args.dir)

def unload(args: Any) -> None:
    watchman_autodef.unload(dir=args.dir)

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', type=Path, default=Path('.'))

subparsers = parser.add_subparsers()
unload_parser = subparsers.add_parser('unload')
unload_parser.set_defaults(main=unload)
update_parser = subparsers.add_parser('update')
update_parser.set_defaults(main=update)

if __name__ == '__main__':
    args = parser.parse_args()
    if not hasattr(args, 'main'):
        parser.print_help()
        exit(1)
    args.main(args)
