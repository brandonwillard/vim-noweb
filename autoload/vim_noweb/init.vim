
if !exists('s:is_enabled')
  let s:is_enabled = 0
endif

function! vim_noweb#init#_initialize() abort

  augroup vim_noweb
    autocmd!
  augroup END

  call vim_noweb#init#_variables()

  if !get(g:, 'vim_noweb#disable_onchange')
    call vim_noweb#onchange#_init()
  endif

endfunction

function! vim_noweb#init#_enable() abort
  let s:is_enabled = 1
endfunction

function! vim_noweb#init#_disable() abort

  augroup vim_noweb
    autocmd!
  augroup END

  let s:is_enabled = 0
endfunction

function! vim_noweb#init#_variables() abort

  if !exists('g:vim_noweb#chunk_pos_enabled_opts')

    ""
    " A code chunk is considered enable by the REPL features when
    "   1. one of the "positive" options in this variable is set to true in the current chunk,
    "   2. one of the positive options is unset and its default is true,
    "   3. none are explicitly set to false in the current chunk.
    "
    let g:vim_noweb#chunk_pos_enabled_opts = {'evaluate': v:true}
  endif 
  if !exists('g:vim_noweb#chunk_neg_enabled_opts')
    ""
    " A code chuk is considered disabled by the REPL features when 
    "   1. one of the "negative" options in this variable is set to true in the current chunk,
    "   2. one of the negative options is unset in the current chunk and has a default of true.
    "
    let g:vim_noweb#chunk_neg_enabled_opts = {'fig': v:false}
  endif

  if !exists('b:noweb_language')
    ""
    " Filetype name for the embedded programming language (e.g. 'python' for
    " Python).
    let b:noweb_language = split(&filetype, '\.')[0]
  endif
  if !exists('b:noweb_backend')
    ""
    " Filetype name for the typesetting language (e.g. 'tex' for [La]TeX).
    let b:noweb_backend = split(&filetype, '\.')[1]
  endif

  if !get(g:, 'vim_noweb#disable_onchange')
    ""
    " If true, disables syntax scope option changes.
    let g:vim_noweb#disable_onchange = 0
    call vim_noweb#onchange#_init_watch_variables()
  endif

endfunction

