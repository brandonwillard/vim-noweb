au! BufRead,BufNewFile *.[Tt]exw
      \ let b:noweb_language='python' | 
      \ let b:noweb_backend='tex' | 
      \ setfiletype texw.noweb 
au! BufRead,BufNewFile *.[Pp]nw
      \ let b:noweb_language='python' | 
      \ let b:noweb_backend='markdown' | 
      \ setfiletype pnw.noweb 
au! BufRead,BufNewFile *.[Rr]md 
      \ let b:noweb_language='r' | 
      \ let b:noweb_backend='markdown' 
      \ setfiletype rnw.noweb 
