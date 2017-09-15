if exists('g:loaded_vim_noweb')
  finish
endif

let g:loaded_vim_noweb = 1

let &runtimepath .= ',' . expand('<sfile>:p:h:h') . '/after'

" vim:foldmethod=marker:foldlevel=0:ts=2:sts=2:sw=2
