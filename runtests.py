#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
import sys
import subprocess
import pytest


PYTEST_ARGS = ['--tb=short', '-q', '-s', '-rw']

FLAKE8_ARGS = ['app', 'tests']

sys.path.append(os.path.dirname(__file__))


def flake8_main(args):
    print('Running lint tests...')
    flake8 = subprocess.call(['flake8'] + args)
    print('\033[91m' + 'Lint flake8 failed' + '\033[0m' if flake8 else
          '\033[92m' + 'Lint flake8 passed' + '\033[0m')
    return flake8


def exit_if_failed(func):
    if func:
        sys.exit(func)


if __name__ == '__main__':
    run_lint = True
    run_pytest = True

    # No lint
    try:
        sys.argv.remove('--nolint')
    except ValueError:
        run_lint = True
    else:
        run_lint = False

    # Lint only
    try:
        sys.argv.remove('--lintonly')
    except ValueError:
        run_pytest = True
    else:
        run_pytest = False

    # Coverage option
    if run_pytest:
        try:
            sys.argv.remove('--coverage')
        except ValueError:
            pass
        else:
            PYTEST_ARGS += [
                '--cov-report', 'html',
                '--cov', 'app']

    # Run flake8 lint
    if run_lint:
        exit_if_failed(flake8_main(FLAKE8_ARGS))

    # Run pytest
    if run_pytest:
        exit_if_failed(pytest.main(PYTEST_ARGS))
