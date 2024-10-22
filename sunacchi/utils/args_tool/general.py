# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/22/24
"""
from argparse import Namespace


def view_args(args: Namespace, args_name: str = None):
    if args_name is None:
        args_name = 'args'

    print(f"{'=' * 15} {args_name} {'=' * 15}")
    for k, v in vars(args).items():
        if v == '':
            print(f"{k} = \'\'")
        else:
            print(f"{k} = {v}")

    print('=' * (30 + len(args_name) + 2))
    print()
