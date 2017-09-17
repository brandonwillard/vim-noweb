if exists('b:noweb_cmdline_loaded') ||
      \ !exists('b:cmdline_source_fun')
  finish
endif

let b:noweb_cmdline_loaded = 1

"
" Wrap an existing source function with a code chunk test.
" XXX: Doesn't work for vimcmdline's send-line commands, since that calls
" nvim's `jobsend` directly.
"
if !exists('b:cmdline_source_fun_backend')
  " echom 'noweb cmdline_source_fun='.string(b:cmdline_source_fun)
  let b:cmdline_source_fun_backend = b:cmdline_source_fun
endif


function! NowebSendChunk(...)
  let l:codelines = vim_noweb#utils#lines_from_chunk(a:000)

  if !empty(l:codelines)
    call b:cmdline_source_fun_backend(l:codelines)

    if a:1 ==? 'down'
      call vim_noweb#utils#goto_next_chunk()
    endif
  endif
endfunction

function! NowebSendFHChunk()

  let l:codelines = vim_noweb#utils#lines_from_here()
  
  if !empty(l:codelines)
    call b:cmdline_source_fun_backend(l:codelines)
  endif
endfunction

function! ReplSendString_noweb(lines)
  if vim_noweb#utils#is_in_code(1) == 0
    return
  else
    return b:cmdline_source_fun_backend(a:lines)
  endif
endfunction

command! NowebSendChunkCmd call NowebSendChunk('stay')
command! NowebSendFHChunkCmd call NowebSendFHChunk()

nnoremap <buffer><silent> <Plug>(noweb-send-chunk) :<C-U>call NowebSendChunk('stay')<CR>
nnoremap <buffer><silent> <Plug>(noweb-send-fh-chunk) :<C-U>call NowebSendFHChunk()<CR>

nmap <buffer> <LocalLeader>tc <Plug>(noweb-send-chunk)
nmap <buffer> <LocalLeader>tC <Plug>(noweb-send-fh-chunk)

" Here's a little custom addition that runs a chunk with the
" name 'pweave_code'.  This can be used to run a weave/build
" command from Python within the REPL session (so that, for example, weaved chunk
" variables are exposed to the session).
nmap <buffer> <LocalLeader>tw :<C-U>call NowebSendChunk('stay', 'pweave_code')<CR>

let b:cmdline_source_fun = function('ReplSendString_noweb')
" let b:cmdline_source_fun = {arg -> function('ReplSendMultiline')(arg)}

" vim:foldmethod=marker:foldlevel=0:ts=2:sts=2:sw=2
