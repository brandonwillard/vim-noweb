
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
    let g:vim_noweb#chunk_pos_enabled_opts = {'evaluate': v:true}
  endif 
  if !exists('g:vim_noweb#chunk_neg_enabled_opts')
    let g:vim_noweb#chunk_neg_enabled_opts = {'fig': v:false}
  endif

  if !exists('b:noweb_language')
    " Handle multi-filetypes (in a very specific way):
    let b:noweb_language = split(&filetype, '\.')[0]
  endif
  if !exists('b:noweb_backend')
    " Handle multi-filetypes (in a very specific way):
    let b:noweb_backend = split(&filetype, '\.')[1]
  endif

  if !get(g:, 'vim_noweb#disable_onchange')
    let g:vim_noweb#disable_onchange = 0
    call vim_noweb#onchange#_init_watch_variables()
  endif
endfunction

