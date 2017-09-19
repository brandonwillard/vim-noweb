import os
import sys
import re
import distutils.util

from io import StringIO

import contextlib

import pweave
from pweave.processors import IPythonProcessor


@contextlib.contextmanager
def capture():
    """ https://stackoverflow.com/a/10743550/3006474
    """
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


class CustomIPythonProcessor(IPythonProcessor):
    """ Disables in-process kernels.

    We need this in order to preserve virtualenv packages in runs of
    Pweave, because an in-process kernel will take the environment of
    the Vim plugin.

    """

    def __init__(self, *args):
        super(IPythonProcessor, self).__init__(*args, embed_kernel=False)

        if pweave.rcParams["usematplotlib"]:
            self.init_matplotlib()


def get_virtualenv_path():
    r""" Add a virtualenv to sys.path so the user can import modules from it.

    This isn't perfect: it doesn't use the Python interpreter with which the
    virtualenv was built, and it ignores the --no-site-packages option. A
    warning will appear suggesting the user installs IPython in the
    virtualenv, but for many cases, it probably works well enough.

    Adapted from code snippets online.

    http://blog.ufsoft.org/2009/1/29/ipython-and-virtualenv

    Returns
    =======
        The adjusted `os.path` variable; otherwise, `None`.
    """

    virtual_env_prefix = os.environ.get('VIRTUAL_ENV', None)

    # See https://stackoverflow.com/a/1883251/3006474
    # XXX: The following doesn't work well when Vim's python is in a
    # vim-specific virtualenv and Vim itself is being run in an entirely
    # different virtualenv.
    # virtual_env_prefix = sys.prefix

    if virtual_env_prefix is None or\
            (not hasattr(sys, 'real_prefix')
             and virtual_env_prefix == sys.base_prefix):
        # Not in a virtualenv
        return None

    # venv detection:
    # stdlib venv may symlink sys.executable, so we can't use realpath.  but
    # others can symlink *to* the venv Python, so we can't just use
    # sys.executable.  So we just check every item in the symlink tree
    # (generally <= 3)
    p = os.path.normcase(sys.executable)
    paths = [p]

    while os.path.islink(p):
        p = os.path.normcase(os.path.join(os.path.dirname(p), os.readlink(p)))
        paths.append(p)

    p_venv = os.path.normcase(virtual_env_prefix)
    if any(p.startswith(p_venv) for p in paths):
        # Running properly in the virtualenv, don't need to do anything
        return

    if sys.platform == "win32":
        virtual_env = os.path.join(virtual_env_prefix, 'Lib',
                                   'site-packages')
    else:
        virtual_env = os.path.join(virtual_env_prefix, 'lib',
                                   'python{}.{}'.format(*sys.version_info[:2]),
                                   'site-packages')

    # import site
    # sys.path.insert(0, virtual_env)
    # site.addsitedir(virtual_env)

    return virtual_env


def parse_noweb_args(line):
    """ Parses a line for a noweb code chunk header
    and extracts the chunk keyword options.

    Chunk headers are delimited by
    ```
    <<chunk_name, option1=value1, ...>>=
    ...
    @
    ```
    This function returns `{"option1":"value1", ...}`.

    Parameters
    ==========
    line: str
        The noweb document line.

    Returns
    =======
    A `dict` with chunk option keywords and their values as strings.
    Otherwise, `None` when the line doesn't contain a valid code chunk header.
    """
    re_expr = re.compile(r'^\s*?<<\w*?\s*?,?\s*?(.*)>>=\s*$')
    chunk_args = re.findall(re_expr, line)

    if len(chunk_args) == 0:
        return None

    import shlex
    sh = shlex.shlex(chunk_args[0], posix=True)
    sh.whitespace = ','
    sh.wordchars += '= '

    chunk_opts = filter(lambda x: '=' in x, sh)
    dict_res = dict(map(str.strip, val.split('=', 1)) for val in chunk_opts)
    return dict_res


def default_is_enabled(x, default):
    try:
        return distutils.util.strtobool(x)
    except ValueError:
        return default


def chunk_enabled(line, pos_options, neg_options, is_enabled=default_is_enabled):
    r""" Check if a noweb code chunk header is enabled for evaluation during the
    weaving phase.

    Parameters
    ==========
    line: str
        The noweb document line.
    pos_options: dict
        The option names determining whether or not a chunk is enabled
        and their default values.
    neg_options: dict
        When these options are enabled, the chunk *shouldn't* be evaluated.
    is_enabled: list of lambdas or functions
        Function(s) used to evaluate whether or not an option is considered
        enabled.

    Returns
    =======
    `True` if the line is a code chunk header that is enabled.

    """
    chunk_opts = parse_noweb_args(line)

    if chunk_opts is None:
        return False

    res = any(is_enabled(chunk_opts.get(opt_name, ''), opt_default)
              for opt_name, opt_default in pos_options.items())

    res &= not any(is_enabled(chunk_opts.get(opt_name, ''), opt_default)
                   for opt_name, opt_default in neg_options.items())
    return res
