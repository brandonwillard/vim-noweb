if exists('b:loaded_rnoweb_ftplugin')
  finish
endif

let b:loaded_rnoweb_ftplugin = 1

let b:noweb_backend='tex'
let b:noweb_language='r'

setl iskeyword+=-

" vim:foldmethod=marker:foldlevel=0
