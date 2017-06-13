" 日本語 wordnet DB から類義語を検索します.
"
scriptencoding utf-8
let s:save_cpo = &cpo
set cpo&vim

pyfile <sfile>:h:h/src/thesaurus.py
python import vim

function! thesaurus#get_synonym(word)
  python thesaurus_get_synonym(vim.eval('a:word'))
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
