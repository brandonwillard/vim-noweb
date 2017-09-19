
let g:cmdline_map_start = "<LocalLeader>tr"
let g:cmdline_map_send = "<LocalLeader>tl"
let g:cmdline_map_send_selection = "<LocalLeader>ts"
let g:cmdline_map_source_fun = "<LocalLeader>tf"
let g:cmdline_map_send_paragraph = "<LocalLeader>tp"
let g:cmdline_map_send_block = "<LocalLeader>tb"
let g:cmdline_map_quit = "<LocalLeader>tq"

let g:cmdline_term_height = -1
let g:cmdline_term_width = -1

let g:cmdline_vsplit = 0
let g:cmdline_esc_term = 1
let g:cmdline_in_buffer = 1 
let g:cmdline_outhl = 0
" let g:cmdline_app = {}

" Custom options
let g:cmdline_nolisted = 1
let g:cmdline_golinedown = 0

" Enable (and likewise disable) bracketed paste mode in the terminal.
let &t_ti .= "\<Esc>[?2004h"
let &t_te .= "\<Esc>[?2004l"

if !exists("g:cmdline_bps")
  let g:cmdline_bps = "\x1b[200~"
endif

if !exists("g:cmdline_bpe")
  let g:cmdline_bpe = "\x1b[201~"
endif

" Use this to set a connection string (e.g. "--existing kernel.json --ssh jupyterhub")
let g:cmdline_jupyter_opts = ""
" Don't use jupyter console app by default.
let g:cmdline_jupyter = 0

exe 'nmap <silent> ' . g:cmdline_map_send . ' <Plug>(cmdline-send-line)'
exe 'vmap <silent> ' . g:cmdline_map_send_selection . ' <Plug>(cmdline-send-selection)'
exe 'nmap <silent> ' . g:cmdline_map_send_selection . ' <Plug>(cmdline-send-selection)'
exe 'vmap <silent> ' . g:cmdline_map_send . ' <Plug>(cmdline-send-lines)'
exe 'nmap <silent> ' . g:cmdline_map_source_fun . ' <Plug>(cmdline-send-file)'
exe 'nmap <silent> ' . g:cmdline_map_send_paragraph . ' <Plug>(cmdline-send-paragraph)'
exe 'nmap <silent> ' . g:cmdline_map_send_block . ' <Plug>(cmdline-send-mblock)'
exe 'nmap <silent> ' . g:cmdline_map_quit . ' <Plug>(cmdline-send-quit)'
exe 'nmap <silent> ' . g:cmdline_map_start . ' <Plug>(cmdline-send-start)'

" XXX: This post setup only loads *once*, so buffer local settings aren't
" reasonable.  That's what the following function does.
" call VimCmdLineCreateMaps()

function! g:ReplSendMultiline(lines)
  " Just for some background, you might see control/escape
  " sequences like `\x1b[200~` printed as `^[[200~`.  The
  " first part is, of course, the ESC control character
  " (ASCII: `^[`).  These exact control sequences are bracketed
  " paste modes in an xterm setting 
  "
  " References:
  " https://cirw.in/blog/bracketed-paste
  " http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
  " http://www.xfree86.org/current/ctlseqs.html
  let expr_str = g:cmdline_bps
  let expr_str .= join(add(a:lines, ''), b:cmdline_nl)
  let expr_str .= g:cmdline_bpe
  let expr_str .= b:cmdline_nl

  call VimCmdLineSendCmd(expr_str)

endfunction

function! g:StartJupyterString(kernel)
  if !executable("jupyter-console")
    return ""
  endif

  let kernels_info = json_decode(system("jupyter-kernelspec list --json"))
  if !has_key(kernels_info['kernelspecs'], a:kernel)
    return ""
  endif

  let jupyter_opts = get(b:, "cmdline_jupyter_opts", get(g:, "cmdline_jupyter_opts", ""))
  let cmd_str = printf("jupyter-console --kernel %s %s", a:kernel, jupyter_opts)
  return cmd_str
endfunction


