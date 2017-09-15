filetype off
let &rtp .= ','.finddir('vim-noweb', ';', 1)
filetype plugin indent on
syntax enable
let g:python_host_prog=expand('~/.pyenv/versions/neovim2/bin/python')
let g:python3_host_prog=expand('~/.pyenv/versions/neovim36/bin/python')

