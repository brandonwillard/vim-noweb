# `vim-noweb`

Tools for noweb files, projects and their development.

## Installation

Requires Neovim with Python 3.

1. Extract the files and put them in your Neovim directory (usually `$XDG_CONFIG_HOME/nvim/`).
2. Execute `:UpdateRemotePlugins` and restart Neovim.

For [`vim-plug`](https://github.com/junegunn/vim-plug)
```viml
Plug 'brandonwillard/vim-noweb', { 'do': ':UpdateRemotePlugins' }
```

## Requirements

`vim-noweb` requires that Neovim be compiled with `python3`.
If `:echo has("python3")` returns `1`, then you're done; otherwise, see below.

You can enable the Python 3 interface with `pip`, e.g.:
```bash
$ pip3 install neovim
```

# Development

The layout/design of this plugin is modeled after [deoplete.nvim](https://github.com/Shougo/deoplete.nvim).

## Documentation

Vimdocs are generated with the Python module [`vimdoc`](https://github.com/google/vimdoc).  Just run `vimdoc`.



