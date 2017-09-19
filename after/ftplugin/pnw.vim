if exists('b:loaded_pnw_ftplugin')
  finish
endif

let b:loaded_pnw_ftplugin = 1

let b:noweb_backend='markdown'
let b:noweb_language='python'

"             *noweb_weave_language*
" noweb_weave_language
"     Name of the Jupyter language kernel for the code in the document's code chunks (e.g. 'python3').
"
"             *noweb_weave_backend*
" noweb_weave_backend
"     Name of the typesetting language in which the code is embedded.  In other words, the file format of the weaving's output.
" 
"             *noweb_format_opts*
" noweb_format_opts
"     Pweave formatter dictionary.  See http://mpastell.com/pweave/customizing.html.
" 
"             *noweb_weave_docmode*
" noweb_weave_docmode
"     Set Pweave's docmode option.
" 
"             *noweb_backend_src_dir*
" noweb_backend_src_dir
"     Location/destination for the resulting backend source file.
" 
"             *noweb_figures_dir*
" noweb_figures_dir
"     Destination for resulting figures.  
" 
"             *noweb_weave_formatter* 
" noweb_weave_formatter
"     Name of the Pweave output format.  See http://mpastell.com/pweave/formats.html.
  
setl makeprg=make\ %:gs?[Pp]nw$?md?:t

" vim:foldmethod=marker:foldlevel=0
