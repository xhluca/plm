import argparse
import os
import subprocess
import sys


def activate_venv(path):
    activate_path = os.path.join(path, "bin", "activate")
    return subprocess.check_call(["/bin/bash", "--rcfile", activate_path])


def create_venv(path):
    return subprocess.check_call([sys.executable, "-m", "venv", path])


def pip_install(packages):
    print(sys.executable)
    return subprocess.check_call([sys.executable, "-m", "pip", "install", *packages])


def pip_uninstall(packages):
    return subprocess.check_call([sys.executable, "-m", "pip", "uninstall", *packages])


def pip_freeze(filename="./requirements.txt"):
    frozen = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    with open(filename, "wb") as f:
        f.write(frozen)


def store_dependency(packages, filename="./dependencies.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = set([l.strip("\n") for l in f.readlines()])
    else:
        lines = set()

    lines.update(packages)

    with open(filename, "w") as f:
        for line in lines:
            f.write(line + os.linesep)


def remove_dependency(packages, filename="./dependencies.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = set([l.strip("\n") for l in f.readlines()])
    else:
        lines = set()

    for package in packages:
        for line in lines:
            if line.startswith(package):
                lines.remove(line)

    with open(filename, "w") as f:
        for line in lines:
            f.write(line + os.linesep)


def _install(args):
    pip_install(args.packages)
    store_dependency(args.packages)
    pip_freeze()


def _uninstall(args):
    pip_uninstall(args.packages)
    remove_dependency(args.packages)
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

    parser_install = subparsers.add_parser(
        "install", aliases=["i"], help="install a package with pip"
    )
    parser_uninstall = subparsers.add_parser(
        "uninstall", help="install a package with pip"
    )
    parser_activate = subparsers.add_parser(
        "activate", help="activate a virtual environment"
    )
    parser_create = subparsers.add_parser(
        "create", help="create a virtual environment with venv"
    )

    parser_activate.add_argument("path", default="./venv/", nargs="?")
    parser_create.add_argument("path", default="./venv/", nargs="?")
    parser_install.add_argument("packages", nargs="+")
    parser_uninstall.add_argument("packages", nargs="+")

    parser.set_defaults(func=_default)
    parser_activate.set_defaults(func=_activate)
    parser_create.set_defaults(func=_create)
    parser_install.set_defaults(func=_install)
    parser_uninstall.set_defaults(func=_uninstall)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()