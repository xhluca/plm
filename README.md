# `plm`

*Helps you manage python libraries and environments*

## Quickstart

```bash
pip3 install git+https://github.com/xhlulu/plm.git
```

Create and activate an environment:
```bash
plm
```
which is equivalent to:
```bash
plm create
plm activate
```

Install a package:
```bash
plm install requests numpy
# also works: plm i requests numpy
```

Now `requests` and `numpy` will be installed in your `venv/` and they will also be in `dependencies.txt` and `requirements.txt`.


## Why would I need `plm`?

Traditionally, to create an environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

Then, to install a library and track dependencies:
```bash
pip3 install requests numpy
echo -e "requests\nnumpy" >> dependencies.txt
pip freeze > requirements.txt
```

Instead, with `plm`, you just need to do this:
```bash
plm create
plm activate
plm i requests numpy
```

## Managing virtual environments

You can customize the name of the venv:
```bash
plm create myvenv
plm activate myvenv
```

## Installing libraries

`plm install` has the shorthand `plm i`. There's many ways to install packages:
```bash
plm install requests
plm i pandas==1.*
plm i numpy Pillow
```
etc.


## dependencies.txt vs requirements.txt

`dependencies.txt` loosely keeps track of your packages, which is good for readability and upgradability. It will be updated every time you pip install a package, e.g. if you run `plm install <package 1> <package 2>` then it will look like this:
```
<old package 1>
...
<old package N>
<package 1>
<package 2>
```

`requirements.txt` on the other hands keeps track of the exact requirements (e.g. for deploying to a server). It's the output of `pip freeze > requirements.txt`.

## Note

`plm`'s not meant as a replacement for `pip` or `venv`, it simply wraps usual/repetitive commands in a easy-to-remember CLI. The codebase is < 100 lines, which makes it ideally for forking and extending. If you are planning to do more serious environment managment, please use `conda`, which also has `conda create` and `conda activate` commands and has significantly more features. If you are planning to do serious dependencies management, use `pipenv` instead.

## Acknowledgement

Commands like `create` `activate` are inspired from `conda`. `install` (or `i`) is inspired from npm.