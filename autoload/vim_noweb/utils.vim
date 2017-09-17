"
" Some of these are borrowed from the Nvim-R plugin.
"
" TODO: Nearly all should be implemented by the Python plugin.
"

function! vim_noweb#utils#is_in_code(vrb)
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

function! vim_noweb#utils#goto_next_chunk() range
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

function! vim_noweb#utils#goto_prev_chunk() range
  let l:rg = range(a:firstline, a:lastline)
  let l:chunk = len(l:rg)
  for var in range(1, l:chunk)
    let l:curline = line('.')
    if vim_noweb#utils#is_in_code(0)
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

function! vim_noweb#utils#lines_from_here()
  let l:begchk = '^<<.*>>=\$'
  let l:endchk = '^@'

  let l:codelines = []
  let l:here = line('.')
  let l:curbuf = getline(1, '$')
  let l:idx = 0

  while l:idx < l:here
    " escape(curbuf[idx], '\\\"'')
    let l:chunk_line = l:curbuf[l:idx]
    
    "if curbuf[idx] =~# begchk
    " if !empty(l:chunk_line)
    let l:enabled = ChunkEnabled(l:chunk_line)
    " endif

    if l:enabled == 1
      let l:idx += 1
      while l:curbuf[l:idx] !~# l:endchk && l:idx < l:here
        let l:codelines += [l:curbuf[l:idx]]
        let l:idx += 1
      endwhile
    else
      let l:idx += 1
    endif
  endwhile

  return l:codelines

endfunction

function! vim_noweb#utils#lines_from_chunk(...)
  " Function that REPLs code chunks.
  " TODO: This should be a Python function.
  " Takes two arguments:
  "     * First is a string value for which "down" signifies that
  "     the cursor is to jump to the next chunk after sending.
  "     * Second is an optional string that matches the first argument/option
  "     of the chunk (i.e. it IDs the chunk).
  let l:chunkline = -1
  let l:docline = -1
  if a:0 > 1
    let l:chunkline = search("^<<\\s*" . a:2, 'bncw') + 1
    if l:chunkline < 2
      echomsg 'Chunk starting with "' . a:2 . '" not found.'
      return []
    endif
    "let l:docline = search('\\%>'.string(l:chunkline-1).'l\\_.\\{-}\\_^@', 'ncwe') - 1
    let l:endchk = '^@'
    let l:codelines = [getline(l:chunkline)]
    while getline(l:chunkline + 1) !~ l:endchk
      let l:chunkline += 1
      let l:codelines += [getline(l:chunkline)]
    endwhile
  else
    if vim_noweb#utils#is_in_code(0) == 0
      echomsg 'Not inside a code chunk.'
      return []
    endif
    let l:chunkline = search('^<<', 'bncW') + 1
    let l:docline = search('^@', 'ncW') - 1
    let l:codelines = getline(l:chunkline, l:docline)
  endif

  return l:codelines

endfunction

" vim:foldmethod=marker:foldlevel=0:ts=2:sts=2:sw=2
