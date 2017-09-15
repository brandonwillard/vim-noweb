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

    # @neovim.command('NowebTestCommand', nargs='*', sync=True)
    # def test_command(self, args):
    #     """ TODO
    #     Parameters
    #     ----------
    #     args: list of str
    #         Arguments passed from `neovim`.
    #     """
    #     logging.info('test command called!')
    #     # self.nvim.current.buffer.options['syntax'] = 'python'
    #     # self.nvim.command('syntax enable')
    #     # buffer = self.nvim.current.buffer
    #     # window = self.nvim.current.window

    @neovim.function("ChunkEnabled", sync=True)
    def chunk_enabled(self, line):
        """ Determines whether or not the current chunk (based on cursor
        location) is enabled (via the chunk options).  A chunk is enabled
        when

            * one of the "positive" options in
            `vim_noweb#chunk_pos_enabled_opts` is set to true in the current
            chunk,
            * one of the positive options is unset and its default is true,
            * none are explicitly set to false in the current chunk,
            * none of the "negative" options in
            `vim_noweb#chunk_neg_enabled_opts` are set to true in the current
            chunk,
            * none of the negative options are unset and have a default of
            true.

        Parameters
        ----------
        line: str
            String containing the chunk's options.
        """

        cur_buf_vars = self.nvim.current.buffer.vars
        pos_enabled_opts = cur_buf_vars.get(
            'vim_noweb#chunk_pos_enabled_opts', {})
        neg_enabled_opts = cur_buf_vars.get(
            'vim_noweb#chunk_neg_enabled_opts', {})

        return chunk_enabled(line, pos_enabled_opts, neg_enabled_opts)
