import argparse
import os

from .__init__ import (
    pip_install,
    store_dependencies,
    pip_freeze,
    pip_uninstall,
    activate_venv,
    create_venv,
    remove_dependencies,
)


def _install(args):
    if len(args.packages) == 0 and args.requirements is not None:
        pip_install(["-r", args.requirements])
    elif len(args.packages) >= 1:
        pip_install(args.packages)
        store_dependencies(args.packages)
        pip_freeze()
    else:
        for filename in ['dependencies.txt','requirements.txt']:
            if os.path.exists(filename):
                pip_install(['-r', filename])
                print(f"Installed all libraries specified in {filename}")
                return
        raise ValueError("Could not find a file named dependencies.txt or requirements.txt, aborting.")


def _uninstall(args):
    pip_uninstall(args.packages)
    remove_dependencies(args.packages)
    pip_freeze()


def _create(args):
    create_venv(args.path)


def _activate(args):
    activate_venv(args.path)


def _default(_):
    create_venv("./venv")
    activate_venv("./venv")


def main():
    parser = argparse.ArgumentParser(
        "Like npm, but for python and using pip/venv", usage="plm <command> [<args>]"
    )

    subparsers = parser.add_subparsers(help="")

    parser_activate = subparsers.add_parser(
        "activate", help="activate a virtual environment"
    )
    parser_create = subparsers.add_parser(
        "create", help="create a virtual environment with venv"
    )
    parser_install = subparsers.add_parser(
        "install", aliases=["i"], help="install a package with pip"
    )
    parser_uninstall = subparsers.add_parser(
        "uninstall", help="install a package with pip"
    )

    parser_activate.add_argument("path", default="./venv/", nargs="?")
    parser_create.add_argument("path", default="./venv/", nargs="?")
    parser_install.add_argument("packages", nargs="*")
    parser_uninstall.add_argument("packages", nargs="+")

    parser_install.add_argument("--requirements", "-r")

    parser.set_defaults(func=_default)
    parser_activate.set_defaults(func=_activate)
    parser_create.set_defaults(func=_create)
    parser_install.set_defaults(func=_install)
    parser_uninstall.set_defaults(func=_uninstall)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()