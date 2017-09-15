"
" The stuff in this file is a hack to get 'dynamic' vim settings.  The
" settings will change depending on the cursor location.
"
" First, we load the standard noweb 'backend' settings,
" save some key option values in local variables,
" then we do the same for the noweb 'language'.
" Now, we can create functions that check the
" cursor location to determine which settings to use.
"
" FIXME: Lame that we have to manually load and list out the settings
" manually for each filetype.  Perhaps we could load these filetypes
" into a scratch buffer and get the values from there.
" TODO: what about the `b:undo_ftplugin` and `b:undo_indent` variables?
" Looks like we could generate the `options_list` from that, no?
" TODO: what about syntax files?  looks like `iskeyword` doesn't work
" because of that.
"
" The OnSyntaxChange plugin (http://www.vim.org/scripts/script.php?script_id=4085)
" provides the mechanism for triggering these changes.
"
function! vim_noweb#onchange#_init() abort

  call vim_noweb#onchange#_set_watch_variables()

  call OnSyntaxChange#Install('NowebCode', 'nowebChunk', 1, 'a')

  augroup vim_noweb
    autocmd User SyntaxNowebCodeEnterA unsilent
          \ call vim_noweb#onchange#_set_lang_settings(b:noweb_language)
    autocmd User SyntaxNowebCodeLeaveA unsilent
          \ call vim_noweb#onchange#_set_lang_settings(b:noweb_backend)
  augroup END

endfunction

function! vim_noweb#onchange#_set_lang_settings(lang) abort
  try
    for l:topt in g:noweb_options_list
      let l:exec_str = 'let &l:'.l:topt.' = b:noweb_'.a:lang.'_'.l:topt
      execute(l:exec_str)
    endfor
  catch
    echoerr v:exception
  endtry
endfunction

function! vim_noweb#onchange#_init_watch_variables() abort
  "
  " These variables specify which options to watch and change relative
  " to the syntax scope.
  "
  if !exists('noweb_options_list')
    let g:noweb_options_list = ['formatexpr', 'includeexpr', 'comments', 'formatprg',
          \'commentstring', 'formatoptions', 'iskeyword', 'cinkeys', 'define', 'conceallevel', 'suffixesadd',
          \'omnifunc', 'keywordprg', 'wildignore', 'include', 'textwidth', 'cinoptions']

    " Append these option subsets
    " TODO: Is there really a need for separate options lists?
    let g:noweb_fold_options = ['foldexpr', 'foldtext', 'foldmethod', 'foldlevel', 'foldopen']
    let g:noweb_indent_options = ['indentexpr', 'indentkeys', 'tabstop', 'shiftwidth',
          \'softtabstop', 'expandtab', 'copyindent', 'preserveindent']

    let g:noweb_options_list += g:noweb_indent_options
  endif

endfunction

function! vim_noweb#onchange#_set_watch_variables() abort
  "
  " Here we set the watched variables.
  "
  " TODO: what about the standard ftplugin files?  Mappings?
  "
  " This might be a way to determine/automate the following:
  " http://vim.wikia.com/wiki/Edit_configuration_files_for_a_filetype
  "
  " TODO: Could temporarily use `au OptionSet` to gather option changes.
  "
  for vlang in [b:noweb_backend, b:noweb_language]
    " Unset values:
    " NOTE: Could just do `:setlocal all&`?
    for topt in g:noweb_options_list
      " echom 'unsetting noweb_'.vlang.'_'.topt.'='.eval('&l:' . topt)
      try
        execute(':setlocal ' . topt . '&')
      catch
        echoerr v:exception . ', unsetting topt=' . topt . ' for ' . vlang
      endtry
    endfor

    " :hi clear
    let &filetype=vlang

    for topt in g:noweb_options_list
      " echom 'setting noweb_'.vlang.'_'.topt.'='.eval('&l:' . topt)
      try
        let b:noweb_{vlang}_{topt} = eval('&l:' . topt)
      catch
        echoerr v:exception . ', setting topt=' . topt . ' for ' . vlang
      endtry
    endfor
  endfor

endfunction

