if exists('b:loaded_noweb_ftplugin')
  finish
endif
let b:loaded_noweb_ftplugin=1

if exists('*textobj#user#plugin')
  call textobj#user#plugin('noweb', {
        \ 'code': {
        \     'pattern': ['^<<.*>>=', '^@'],
        \     'select-a': 'aC',
        \     'select-i': 'iC',
        \   }
        \ })
endif

function! NowebIsInCode(vrb)
  let l:chunkline = search('^<<', 'bncW')
  let l:docline = search('^@', 'bncW')
  if l:chunkline > l:docline && l:chunkline != line('.')
    return 1
  else
    if a:vrb
      echomsg 'Not inside a code chunk.'
    endif
    return 0
  endif
endfunction

function! NowebNextChunk() range
  let l:rg = range(a:firstline, a:lastline)
  let l:chunk = len(l:rg)
  for var in range(1, l:chunk)
    let l:i = search('^<<.*$', 'nW')
    if l:i == 0
      echomsg 'There is no next code chunk to go to.'
      return
    else
      call cursor(l:i+1, 1)
    endif
  endfor
  return
endfunction

function! NowebPreviousChunk() range
  let l:rg = range(a:firstline, a:lastline)
  let l:chunk = len(l:rg)
  for var in range(1, l:chunk)
    let l:curline = line('.')
    if NowebIsInCode(0)
      let l:i = search('^<<.*$', 'bnW')
      if l:i != 0
        call cursor(l:i-1, 1)
      endif
    endif
    let l:i = search('^<<.*$', 'bnW')
    if l:i == 0
      call cursor(l:curline, 1)
      echomsg 'There is no previous code chunk to go to.'
      return
    else
      call cursor(l:i+1, 1)
    endif
  endfor
  return
endfunction
" }}}

" Chunk mappings {{{
nnoremap <buffer><silent> <Plug>(noweb-prev-chunk) :<C-U>call NowebPreviousChunk()<CR>
nnoremap <buffer><silent> <Plug>(noweb-next-chunk) :<C-U>call NowebNextChunk()<CR>

nmap <buffer> <LocalLeader>gN <Plug>(noweb-prev-chunk)
nmap <buffer> <LocalLeader>gn <Plug>(noweb-next-chunk)
" }}}

" The following is a hack to get 'dynamic' vim settings.  The settings
" will change depending on the cursor location.
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
call OnSyntaxChange#Install('NowebCode', 'nowebChunk', 1, 'a')

if !exists('b:noweb_language')
  " Handle multi-filetypes (in a very specific way):
  let b:noweb_language = split(&filetype, '\.')[0]
endif
if !exists('b:noweb_backend')
  " Handle multi-filetypes (in a very specific way):
  let b:noweb_backend = split(&filetype, '\.')[1]
endif

augroup noweb_onsyntax
  autocmd!
  autocmd User SyntaxNowebCodeEnterA unsilent call SetCodeSettings(b:noweb_language)
  autocmd User SyntaxNowebCodeLeaveA unsilent call SetCodeSettings(b:noweb_backend)
augroup END

let b:noweb_options_list = ['formatexpr', 'includeexpr', 'comments', 'formatprg',
      \'commentstring', 'formatoptions', 'iskeyword', 'cinkeys', 'define', 'conceallevel',
      \'omnifunc', 'keywordprg', 'wildignore', 'include', 'textwidth', 'cinoptions']

" Append these option subsets
let s:noweb_fold_options = ['foldexpr', 'foldtext', 'foldmethod', 'foldlevel', 'foldopen']
let s:noweb_indent_options = ['indentexpr', 'indentkeys', 'tabstop', 'shiftwidth',
      \'softtabstop', 'expandtab', 'copyindent', 'preserveindent']

let b:noweb_options_list += s:noweb_indent_options
let b:noweb_lang_settings = ''

function! SetCodeSettings(lang)
  " echom "setting " . a:lang . " settings"
  if b:noweb_lang_settings ==? '' || b:noweb_lang_settings !=? a:lang
    let b:noweb_lang_settings = a:lang
    try
      for l:topt in b:noweb_options_list
        let l:exec_str = 'let &l:'.l:topt.' = b:noweb_'.a:lang.'_'.l:topt
        execute(l:exec_str)
      endfor
    catch
      echoerr v:exception
    endtry
  endif
endfunction

" TODO: what about the standard ftplugin files?
" This might be a way to determine/automate the following:
" http://vim.wikia.com/wiki/Edit_configuration_files_for_a_filetype
"
for vlang in [b:noweb_backend, b:noweb_language]
  " try
  " Unset values:
  " NOTE: Could just do `:set all&`.
  for topt in b:noweb_options_list
    " echom "unsetting noweb_".vlang."_".topt."=".eval("&l:" . topt)
    try
      execute(':set '.topt.'&')
    catch
      echoerr v:exception . ', topt=' . topt
    endtry
  endfor

  " :hi clear
  let &filetype=vlang

  for topt in b:noweb_options_list
    " echom "setting noweb_".vlang."_".topt."=".eval("&l:" . topt)
    try
      let b:noweb_{vlang}_{topt} = eval('&l:' . topt)
    catch
      echoerr v:exception . ', topt=' . topt
    endtry
  endfor
  " catch
  "   echoerr v:exception
  " endtry
endfor
let &filetype='noweb'

"let g:ft_ignore_pat = s:old_ft_ignore_pat
"let did_load_filetypes = 1

" vim:foldmethod=marker:foldlevel=0:ts=2:sts=2:sw=2:et
