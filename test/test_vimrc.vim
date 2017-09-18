filetype off

let &runtimepath .= ','.finddir('vim-noweb', ';', 1)

" set runtimepath+=~/projects/code/vim-plugins/vimcmdline/

let g:python3_host_prog=expand('$VIRTUAL_ENV/bin/python')

" let g:mapleader='\'
" let g:maplocalleader=','

filetype plugin on
" syntax enable

" source cmdline_setup.vim
