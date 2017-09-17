import os
import traceback

import neovim

import pweave

from .utils import chunk_enabled, capture


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

    def _get_any_var(self, name, default=None):
        """ Get a variable from buffer scope, if it's not there,
        get it from global; otherwise, return a given default value.
        """
        g_vars = self.nvim.vars
        b_vars = self.nvim.current.buffer.vars

        return b_vars.get(name, g_vars.get(name, default))

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
    def nvim_chunk_enabled(self, line):
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

        # line = map(methodcaller('decode', self.nvim.eval('&encoding')), line)
        line = line[0]

        # logging.info("chunk_enabled-{}".format(line))
        # cur_vars = self.nvim.current.buffer.vars

        pos_enabled_opts = self._get_any_var(
            'vim_noweb#chunk_pos_enabled_opts', {})
        neg_enabled_opts = self._get_any_var(
            'vim_noweb#chunk_neg_enabled_opts', {})

        return chunk_enabled(line, pos_enabled_opts, neg_enabled_opts)

    @neovim.command("NowebWeave", nargs=0, sync=True)
    def nvim_weave_file(self, *args, **kwargs):
        """ Weaves the current buffer with Pweave.

        The weaving process relies on a few vim variables:

            * `noweb_weave_language`: name of the Jupyter language kernel for
            the code in the document's code chunks (e.g. 'python3').
            * `noweb_weave_backend`: name of the typesetting language in which
            the code is embedded.  In other words, the file format of the
            weaving's output.
            * `noweb_format_opts`: Pweave formatter dictionary.
            See http://mpastell.com/pweave/customizing.html.
            * `noweb_weave_docmode`: Set Pweave's docmode option.
            * `noweb_backend_src_dir`: Location/destination for the
            resulting backend source file.
            * `noweb_figures_dir`: Destination for resulting figures.
            * `noweb_weave_formatter`: Name of the Pweave output
            format.  See http://mpastell.com/pweave/formats.html.

        If you would like to add new Pweave formats or change default
        Pweave values, make these changes via the standard Pweave route
        (e.g. http://mpastell.com/pweave/defaults.html)
        using Vim's Python capabilities (e.g. `:python ...`)
        *after* this plugin has loaded.

        """

        currbuf = self.nvim.current.buffer

        weave_format_opts = self._get_any_var('noweb_format_opts',
                                              {'width': r'\linewidth'})

        weave_kernel = self._get_any_var('noweb_weave_language', None)
        if weave_kernel is None:
            weave_kernel = self._get_any_var('noweb_language', None)

        file_out_ext = self._get_any_var('noweb_weave_backend', None)
        if file_out_ext is None:
            file_out_ext = self._get_any_var('noweb_backend', None)

        weave_docmode = self._get_any_var('noweb_weave_docmode', True)

        backend_src_dir = self._get_any_var('noweb_backend_src_dir', './')
        figures_dir = self._get_any_var('noweb_figures_dir', './')

        # TODO: Could also use `g:vimtex_latexmk_build_dir`.
        # build_dir = self._get_any_var('latex_build_dir', './')

        project_dir, input_file = os.path.split(currbuf.name)
        input_file_base, input_file_ext = os.path.splitext(input_file)
        output_filename = input_file_base + os.path.extsep + file_out_ext

        output_file = os.path.join(backend_src_dir, output_filename)

        pweave.rcParams['figdir'] = figures_dir
        pweave.rcParams['storeresults'] = weave_docmode

        # E.g. 'texmintedpandoc'
        weave_formatter = self._get_any_var('noweb_weave_formatter')

        formats_mod = pweave.formatters.PwebFormats
        formatter_cls = formats_mod.formats.get(weave_formatter, None)

        if formatter_cls is None:
            weave_formatter = formats_mod.guessFromExtension(file_out_ext)
            formatter_cls = formats_mod.formats.get(weave_formatter)

        weaver = pweave.Pweb(input_file,
                             doctype=file_out_ext,
                             kernel=weave_kernel,
                             output=output_file,
                             figdir=figures_dir)

        weaver.documentationmode = weave_docmode

        weaver.setformat(Formatter=formatter_cls['class'])

        if weave_format_opts is not None:
            weaver.updateformat(weave_format_opts)

        try:
            # XXX: If we let Pweave output as it likes, apparently Neovim's RPC
            # gets too upset.
            with capture() as out:
                weaver.weave()
        except Exception as e:
            for line in traceback.format_exc().splitlines():
                self.nvim.err_write("{}\n".format(line))

        # FYI: Gotta add those newlines; otherwise, Neovim won't flush the
        # message.
        self.nvim.out_write("{}\n".format(out[0]))
        self.nvim.err_write("{}\n".format(out[1]))

        # TODO: Populate quickfix with weave output?

    # TODO:
    # function! vim_noweb#utils#is_in_code(vrb)
    #   let l:chunkline = search('^<<', 'bncW')
    #   let l:docline = search('^@', 'bncW')
    #   if l:chunkline > l:docline && l:chunkline != line('.')
    #     return 1
    #   else
    #     if a:vrb
    #       echomsg 'Not inside a code chunk.'
    #     endif
    #     return 0
    #   endif
    # endfunction

    # TODO:
    # function! vim_noweb#utils#goto_next_chunk() range
    #   let l:rg = range(a:firstline, a:lastline)
    #   let l:chunk = len(l:rg)
    #   for var in range(1, l:chunk)
    #     let l:i = search('^<<.*$', 'nW')
    #     if l:i == 0
    #       echomsg 'There is no next code chunk to go to.'
    #       return
    #     else
    #       call cursor(l:i+1, 1)
    #     endif
    #   endfor
    #   return
    # endfunction

    # TODO:
    # function! vim_noweb#utils#goto_prev_chunk() range
    #   let l:rg = range(a:firstline, a:lastline)
    #   let l:chunk = len(l:rg)
    #   for var in range(1, l:chunk)
    #     let l:curline = line('.')
    #     if vim_noweb#utils#is_in_code(0)
    #       let l:i = search('^<<.*$', 'bnW')
    #       if l:i != 0
    #         call cursor(l:i-1, 1)
    #       endif
    #     endif
    #     let l:i = search('^<<.*$', 'bnW')
    #     if l:i == 0
    #       call cursor(l:curline, 1)
    #       echomsg 'There is no previous code chunk to go to.'
    #       return
    #     else
    #       call cursor(l:i+1, 1)
    #     endif
    #   endfor
    #   return
    # endfunction

    # TODO:
    # function! vim_noweb#utils#lines_from_here()
    #   let l:begchk = '^<<.*>>=\$'
    #   let l:endchk = '^@'
    #   let l:codelines = []
    #   let l:here = line('.')
    #   let l:curbuf = getline(1, '$')
    #   let l:idx = 0
    #   while l:idx < l:here
    #     " escape(curbuf[idx], '\\\"'')
    #     let l:chunk_line = l:curbuf[l:idx]
    #     "if curbuf[idx] =~# begchk
    #     " if !empty(l:chunk_line)
    #     let l:enabled = ChunkEnabled(l:chunk_line)
    #     " endif
    #     if l:enabled == 1
    #       let l:idx += 1
    #       while l:curbuf[l:idx] !~# l:endchk && l:idx < l:here
    #         let l:codelines += [l:curbuf[l:idx]]
    #         let l:idx += 1
    #       endwhile
    #     else
    #       let l:idx += 1
    #     endif
    #   endwhile
    #   return l:codelines
    # endfunction

    # TODO:
    # function! vim_noweb#utils#lines_from_chunk(...)
    #   " Function that REPLs code chunks.
    #   " TODO: This should be a Python function.
    #   " Takes two arguments:
    #   "     * First is a string value for which "down" signifies that
    #   "     the cursor is to jump to the next chunk after sending.
    #   "     * Second is an optional string that matches the first argument/option
    #   "     of the chunk (i.e. it IDs the chunk).
    #   let l:chunkline = -1
    #   let l:docline = -1
    #   if a:0 > 1
    #     let l:chunkline = search("^<<\\s*" . a:2, 'bncw') + 1
    #     if l:chunkline < 2
    #       echomsg 'Chunk starting with "' . a:2 . '" not found.'
    #       return []
    #     endif
    #     "let l:docline = search('\\%>'.string(l:chunkline-1).'l\\_.\\{-}\\_^@', 'ncwe') - 1
    #     let l:endchk = '^@'
    #     let l:codelines = [getline(l:chunkline)]
    #     while getline(l:chunkline + 1) !~ l:endchk
    #       let l:chunkline += 1
    #       let l:codelines += [getline(l:chunkline)]
    #     endwhile
    #   else
    #     if vim_noweb#utils#is_in_code(0) == 0
    #       echomsg 'Not inside a code chunk.'
    #       return []
    #     endif
    #     let l:chunkline = search('^<<', 'bncW') + 1
    #     let l:docline = search('^@', 'ncW') - 1
    #     let l:codelines = getline(l:chunkline, l:docline)
    #   endif
    #   return l:codelines
    # endfunction
