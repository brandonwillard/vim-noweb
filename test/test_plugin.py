
import os
import sys
import tempfile

import neovim


def test_weave():
    """ Test weaving for a TeX + Python Noweb file via the Vim command.
    This simply tests whether or not a weaved file (i.e. `*.tex`) was generated.
    """
    tmp_dir = tempfile.gettempdir()

    env_args = ['/usr/bin/env',
                'NVIM_PYTHON_LOG_LEVEL=DEBUG',
                'XDG_CONFIG_HOME={}'.format(tmp_dir),
                'VIMINIT={}'.format(tmp_dir),
                'NVIM_RPLUGIN_MANIFEST={}/rplugin.vim'.format(tmp_dir),
                'NVIM_PYTHON_LOG_FILE={}/nvim_python_log'.format(tmp_dir)]

    child_args = ['/usr/bin/nvim', '-Nu', 'test_vimrc.vim',
                  '+UpdateRemotePlugins', '--embed']

    nvim_args = env_args + child_args

    # print(" ".join(nvim_args))

    nvim = neovim.attach('child', argv=nvim_args)

    # Send an <Enter> keypress to get past opening messages[?]
    nvim.input('\r')
    # nvim.command_output('messages')

    nvim.command_output('edit test_file.texw')

    assert os.path.split(nvim.current.buffer.name)[-1] == 'test_file.texw'

    nvim.current.buffer.vars['noweb_weave_language'] = 'python3'

    if os.path.isfile('test_file.tex'):
        os.remove('test_file.tex')

    if os.path.isdir('cache'):
        import shutil
        shutil.rmtree('cache')

    nvim.command_output(':NowebWeave')

    # DEBUG: Starting here.
    # nvim.eval('v:errmsg')
    # nvim.eval('v:exception')
    # nvim.eval('v:errors')
    # nvim.command_output(':messages')

    assert os.path.isfile("test_file.tex")


def test_chunk_enabled():

    # sys.path.append("./rplugin/python/")

    import vim_noweb  # noqa

    child_argv = ['nvim', '-Nu', 'test_vimrc.vim',
                  '+UpdateRemotePlugins', '--embed']

    nvim = neovim.attach('child', argv=child_argv)
    plugin_obj = vim_noweb.plugin.VimNowebPlugin(nvim)

    # No buffer-local variables are set.
    # cur_buf_vars = nvim.current.buffer.vars
    try:
        nvim.input(':unlet b:vim_noweb#chunk_pos_enabled_opts')
    except nvim.error:
        pass
    try:
        nvim.input(':unlet b:vim_noweb#chunk_neg_enabled_opts')
    except nvim.error:
        pass

    assert not plugin_obj.chunk_enabled('<<blah>>=')
    assert not plugin_obj.chunk_enabled('<<blah, evaluate=False>>=')
    assert not plugin_obj.chunk_enabled('<<blah, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=False, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=True, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=False>>=')

    # Buffer-local variables are set empty.
    cur_buf_vars = nvim.current.buffer.vars
    cur_buf_vars['vim_noweb#chunk_pos_enabled_opts'] = {}
    cur_buf_vars['vim_noweb#chunk_neg_enabled_opts'] = {}

    assert not plugin_obj.chunk_enabled('<<blah>>=')
    assert not plugin_obj.chunk_enabled('<<blah, evaluate=False>>=')
    assert not plugin_obj.chunk_enabled('<<blah, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=False, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=True, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=False>>=')

    # Buffer-local variables are set with default enabled.
    cur_buf_vars['vim_noweb#chunk_pos_enabled_opts'] = {'evaluate': True}
    cur_buf_vars['vim_noweb#chunk_neg_enabled_opts'] = {'fig': False}

    assert plugin_obj.chunk_enabled('<<blah>>=')
    assert plugin_obj.chunk_enabled('<<blah, evaluate=True>>=')
    assert plugin_obj.chunk_enabled('<<blah, fig=False, evaluate=True>>=')
    assert plugin_obj.chunk_enabled('<<blah, fig=False>>=')
    assert not plugin_obj.chunk_enabled('<<blah, evaluate=False>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=True, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=True>>=')

    # Buffer-local variables are set with default disabled.
    cur_buf_vars['vim_noweb#chunk_pos_enabled_opts'] = {'evaluate': False}
    cur_buf_vars['vim_noweb#chunk_neg_enabled_opts'] = {'fig': False}

    assert not plugin_obj.chunk_enabled('<<blah>>=')
    assert plugin_obj.chunk_enabled('<<blah, evaluate=True>>=')
    assert plugin_obj.chunk_enabled('<<blah, fig=False, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=False>>=')
    assert not plugin_obj.chunk_enabled('<<blah, evaluate=False>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=True, evaluate=True>>=')
    assert not plugin_obj.chunk_enabled('<<blah, fig=True>>=')

