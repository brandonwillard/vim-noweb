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
