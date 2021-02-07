import os
import re
import subprocess
import sys


def read_dependencies(filename: str):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return [l.strip("\n") for l in f.readlines()]
    else:
        return []


def write_dependencies(dependencies: list, filename: str):
    with open(filename, "w") as f:
        for line in dependencies:
            f.write(line + os.linesep)


def deps_to_dict(dependencies: list) -> dict:
    splitted = [re.split("(==|>|<|~=)", x) for x in dependencies]
    dep_dict = {d[0].strip(): "".join(d[1:]) for d in splitted}

    return dep_dict


def dict_to_dep_list(dep_dict: dict) -> list:
    return [k + v for k, v in dep_dict.items()]


def python_exec():
    venv_path = os.getenv("VIRTUAL_ENV")
    if venv_path is None:
        return sys.executable
    else:
        return os.path.join(venv_path, "bin", "python")


def activate_venv(path):
    current_venv = os.getenv("VIRTUAL_ENV")
    if current_venv:
        print(
            f'You are currently in a virtual environment at "{current_venv}". Please exit with "deactivate" before activating a new one.'
        )
        return

    activate_path = os.path.join(path, "bin", "activate")
    error_message = f"Unable to find {activate_path}. Are you sure you that {path} is the correct path to your virtual environment?"
    if not os.path.exists(activate_path):
        raise ValueError(error_message)

    print(f'Activated your virtual environment at "{path}"')
    return subprocess.check_call(["/bin/bash", "--rcfile", activate_path])


def create_venv(path):
    if os.path.isdir(path):
        print(
            f'A virtual environment already exists at "{path}". Delete the current one "rm -r {path}" before creating a new environment'
        )
        return

    out = subprocess.check_call([python_exec(), "-m", "venv", path])
    print(f'Created a new virtual environment at "{path}"')
    return out


def pip_install(libraries: list):
    return subprocess.check_call([python_exec(), "-m", "pip", "install", *libraries])


def pip_uninstall(libraries: list):
    return subprocess.check_call([python_exec(), "-m", "pip", "uninstall", *libraries])


def pip_freeze(filename="./requirements.txt"):
    frozen = subprocess.check_output([python_exec(), "-m", "pip", "freeze"])
    with open(filename, "wb") as f:
        f.write(frozen)


def store_dependencies(libraries: list, filename="./dependencies.txt"):
    dependencies = read_dependencies(filename)
    deps_dict = deps_to_dict(dependencies)
    libraries_dict = deps_to_dict(libraries)
    deps_dict.update(libraries_dict)
    new_dependencies = dict_to_dep_list(deps_dict)
    write_dependencies(new_dependencies, filename)


def remove_dependencies(libraries: list, filename="./dependencies.txt"):
    dependencies = read_dependencies(filename)
    deps_dict = deps_to_dict(dependencies)
    libraries_dict = deps_to_dict(libraries)
    new_deps_dict = {}

    for d in deps_dict:
        if d not in libraries_dict:
            new_deps_dict[d] = deps_dict[d]

    new_dependencies = dict_to_dep_list(new_deps_dict)

    write_dependencies(new_dependencies, filename)
