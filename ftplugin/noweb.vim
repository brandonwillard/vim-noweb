if exists('b:loaded_noweb_ftplugin')
  finish
endif

let b:loaded_noweb_ftplugin=1

" Misc Settings {{{
if exists('*textobj#user#plugin')
  call textobj#user#plugin('noweb', {
        \ 'code': {
        \     'pattern': ['^<<.*>>=', '^@'],
        \     'select-a': 'aC',
        \     'select-i': 'iC',
        \   }
        \ })
endif
" }}}

" Chunk mappings {{{
nnoremap <buffer><silent> <Plug>(noweb-prev-chunk) :<C-U>call vim_noweb#utils#goto_prev_chunk()<CR>
nnoremap <buffer><silent> <Plug>(noweb-next-chunk) :<C-U>call vim_noweb#utils#goto_next_chunk()<CR>

if !get(g:, 'noweb_disable_maps', 0)
  nmap <buffer> <LocalLeader>gN <Plug>(noweb-prev-chunk)
  nmap <buffer> <LocalLeader>gn <Plug>(noweb-next-chunk)
endif
" }}}

let s:orig_filetype = &filetype

call vim_noweb#initialize()

" FIXME: Why isn't after/ftplugin being called?  Is it because
" we're switching around filetypes?

let &filetype = s:orig_filetype " 'noweb'

let g:did_load_filetypes = 1

" vim:foldmethod=marker:foldlevel=0:ts=2:sts=2:sw=2:et
