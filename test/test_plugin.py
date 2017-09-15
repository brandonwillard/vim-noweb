
import os
import sys
import json
import neovim

# sys.path.append("./rplugin/python/")

import vim_noweb  # noqa


def test_chunk_enabled():

    child_argv = ["nvim", "-Nu", "test_vimrc.vim",
                  "+UpdateRemotePlugins", "--embed"]

    nvim = neovim.attach('child', argv=child_argv)
    plugin_obj = vim_noweb.plugin.VimNowebPlugin(nvim)

    # No buffer-local variables are set.
    # cur_buf_vars = nvim.current.buffer.vars
    try:
        nvim.input(":unlet b:vim_noweb#chunk_pos_enabled_opts")
    except nvim.error:
        pass
    try:
        nvim.input(":unlet b:vim_noweb#chunk_neg_enabled_opts")
    except nvim.error:
        pass

    assert not plugin_obj.chunk_enabled("<<blah>>=")
    assert not plugin_obj.chunk_enabled("<<blah, evaluate=False>>=")
    assert not plugin_obj.chunk_enabled("<<blah, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=False, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=True, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=False>>=")

    # Buffer-local variables are set empty.
    cur_buf_vars = nvim.current.buffer.vars
    cur_buf_vars['vim_noweb#chunk_pos_enabled_opts'] = {}
    cur_buf_vars['vim_noweb#chunk_neg_enabled_opts'] = {}

    assert not plugin_obj.chunk_enabled("<<blah>>=")
    assert not plugin_obj.chunk_enabled("<<blah, evaluate=False>>=")
    assert not plugin_obj.chunk_enabled("<<blah, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=False, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=True, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=False>>=")

    # Buffer-local variables are set with default enabled.
    cur_buf_vars['vim_noweb#chunk_pos_enabled_opts'] = {'evaluate': True}
    cur_buf_vars['vim_noweb#chunk_neg_enabled_opts'] = {'fig': False}

    assert plugin_obj.chunk_enabled("<<blah>>=")
    assert plugin_obj.chunk_enabled("<<blah, evaluate=True>>=")
    assert plugin_obj.chunk_enabled("<<blah, fig=False, evaluate=True>>=")
    assert plugin_obj.chunk_enabled("<<blah, fig=False>>=")
    assert not plugin_obj.chunk_enabled("<<blah, evaluate=False>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=True, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=True>>=")

    # Buffer-local variables are set with default disabled.
    cur_buf_vars['vim_noweb#chunk_pos_enabled_opts'] = {'evaluate': False}
    cur_buf_vars['vim_noweb#chunk_neg_enabled_opts'] = {'fig': False}

    assert not plugin_obj.chunk_enabled("<<blah>>=")
    assert plugin_obj.chunk_enabled("<<blah, evaluate=True>>=")
    assert plugin_obj.chunk_enabled("<<blah, fig=False, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=False>>=")
    assert not plugin_obj.chunk_enabled("<<blah, evaluate=False>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=True, evaluate=True>>=")
    assert not plugin_obj.chunk_enabled("<<blah, fig=True>>=")

