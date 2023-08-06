# Clone repo and install project in editable mode
Use this installation method if you plan to modify or develop
`pygstuff` (which is likely given the *Development Status* of
`pygstuff`). This way any changes to your local repository are picked
up without having to reinstall `pygstuff`.

**install from your repository clone** by using the `-e` flag.

Enter the `pygstuff` project folder:

```bash
$ cd foo/pygstuff
```

*`foo` is whatever directory `pygstuff` was cloned in*

And install `pygstuff` in *editable* mode:

```bash
$ pip install -e .
```

- the `-e` is short for `--editable`
- the `.` is the path to the project folder
    - (`.` means present working directory)
    - pip finds the `setup.py` file in the `pygstuff` project folder
    - the project folder is the present working directory

This is like `pip install`, but it places a *symbolic link* in
the Python install folder *instead of the actual project files*.

Check this with `pip show` command:

```bash
$ pip show pygstuff
```

See how the `Location` field shows the local repository path
rather than the usual `site-packages` install path.

This means that edits to the source code are immediately
reflected on the next `import pygstuff`, without having to reinstall
the package.

# Clone repo and add foo/pygstuff to PYTHONPATH

If cloning into directory `foo`, add `foo/pygstuff` to the
PYTHONPATH.

## Edit PYTHONPATH on Windows

On Windows, add to the PYTHONPATH for the rest of the PowerShell
session:

```powershell
> $env:PYTHONPATH += "path_to_foo\pygstuff;"
```

Apply this change to every PowerShell session by putting the
above line in the PowerShell Profile.

## Editing PYTHONPATH on Linux

In a pure POSIX environment (Linux), add to the PYTHONPATH with:

```bash
$ PYTHONPATH+="path_to_foo/pygstuff:"
```

Or apply to every `bash` session by editing the ~/.bashrc:

```bash
PYTHONPATH+="path_to_foo/pygstuff:"
export PYTHONPATH
```

## On Cygwin just use the Windows Python Installation

On Cygwin (a POSIX layer on top of Windows) I recommend editing
the PYTHONPATH for Windows only and then running the Windows
Python installation when running Python from Cygwin.

The reason is that Cygwin cannot access the USB ports with the
`pyserial` package. So I end up running the Windows Python
(`python.exe`) from within Cygwin, as opposed to the Python
installed for Cygwin (Cygwin is perfectly happy running any
Windows executable). PYTHONPATH is formatted differently on POSIX
and Windows (path splitter ; vs : and slash direction \ vs /), so
editing PYTHONPATH in the Cygwin `.bashrc` just mangles PYTHONPATH
and makes it unusable by either Python installation.

## Why the path is foo/pygstuff

The way this works is that Python looks in the folders in
PYTHONPATH for a folder containing an `__init__.py`. The
`__init__.py` is in `pygstuff/pygstuff`. The first `pygstuff` is the PyPI
project name, the second `pygstuff` is the package name. So adding
`foo/pygstuff` to the PYTHONPATH, Python looks in the `pygstuff` project
folder and finds the `pygstuff` package folder.

## Clone into USERSITE and add USERSITE/pygstuff to PYTHONPATH

Add `USERSITE/pygstuff` to the PYTHONPATH variable (replacing
USERSITE with the actual USERSITE path).

`USERSITE` is different for every Python installation.

Find the `USERSITE` path with:

```bash
$ python -m site --user-site
```

(Create the `USERSITE` path if it does not exist.)

I like developing packages directly in `USERSITE`. This way I
don't need to edit PYTHONPATH and my packages are visible to
Python.

Unfortunately, because of how PyPI projects are structured,
cloning a *project* to `USERSITE` does not work the same way.

The package is one level deeper: project/package. So Python looks
in USERSITE and does not detect a package because the `project/`
folder does not contain the `__init__.py` file.

On many projects, the package is two levels deeper because the
project is structured `project/src/package/`. In this case, add
`foo/project/src` to PYTHONPATH.
