import argparse
import json
import math
import os
from typing import Optional
from typing import Sequence
from typing import Set

from pre_commit_hooks.util import added_files
from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def lfs_files() -> Set[str]:
    try:
        # Introduced in git-lfs 2.2.0, first working in 2.2.1
        lfs_ret = cmd_output('git', 'lfs', 'status', '--json')
    except CalledProcessError:  # pragma: no cover (with git-lfs)
        lfs_ret = '{"files":{}}'

    return set(json.loads(lfs_ret)['files'])


def find_large_added_files(
        filenames: Sequence[str],
        maxkb: int,
        *,
        enforce_all: bool = False,
) -> int:
    # Find all added files that are also in the list of files pre-commit tells
    # us about
    retv = 0
    filenames_filtered = set(filenames) - lfs_files()
    if not enforce_all:
        filenames_filtered &= added_files()

    for filename in filenames_filtered:
        kb = int(math.ceil(os.stat(filename).st_size / 1024))
        if kb > maxkb:
            print(f'{filename} ({kb} KB) exceeds {maxkb} KB.')
            retv = 1

    return retv


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    parser.add_argument(
        '--enforce-all', action='store_true',
        help='Enforce all files are checked, not just staged files.',
    )
    parser.add_argument(
        '--maxkb', type=int, default=500,
        help='Maxmimum allowable KB for added files',
    )
    args = parser.parse_args(argv)

    return find_large_added_files(
        args.filenames,
        args.maxkb,
        enforce_all=args.enforce_all,
    )


if __name__ == '__main__':
    exit(main())
