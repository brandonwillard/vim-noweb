if exists('b:loaded_pnw_ftplugin')
  finish
endif

let b:loaded_pnw_ftplugin = 1

let b:noweb_backend='markdown'
let b:noweb_language='python'

" TODO: Use projectionist
setl makeprg=make\ %:gs?[Pp]nw$?md?:t

" vim:foldmethod=marker:foldlevel=0
