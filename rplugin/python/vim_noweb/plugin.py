import logging

import neovim

from .utils import chunk_enabled


@neovim.plugin
class VimNowebPlugin:

    def __init__(self, nvim):
        """Initialize plugin

        Parameters
        ---------
        nvim: object
            The `neovim` communication channel.
        """
        self.nvim = nvim.with_decode()

    @neovim.command('NowebTestCommand', nargs='*', sync=True)
    def test_command(self, args):
        """ TODO

        Parameters
        ----------
        args: list of str
            Arguments passed from `neovim`.
        """
        logging.info('test command called!')

        # self.nvim.current.buffer.options['syntax'] = 'python'
        # self.nvim.command('syntax enable')
        # buffer = self.nvim.current.buffer
        # window = self.nvim.current.window

    @neovim.function("ChunkEnabled", sync=True)
    def chunk_enabled(self, line):

        cur_buf_vars = self.nvim.current.buffer.vars
        pos_enabled_opts = cur_buf_vars.get('noweb_chunk_pos_enabled_opts', {})
        neg_enabled_opts = cur_buf_vars.get('noweb_chunk_neg_enabled_opts', {})

        return chunk_enabled(line, pos_enabled_opts, neg_enabled_opts)

        # let enabled = pyeval("chunk_enabled('".escape(curbuf[idx], "\\\"'")."', vim.current.buffer.vars.get('noweb_chunk_pos_enabled_opts', {}), vim.current.buffer.vars.get('noweb_chunk_neg_enabled_opts', {}))")


