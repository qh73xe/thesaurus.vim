scriptencoding utf-8
if exists("g:loaded_thesaurus")
  finish
endif
let g:loaded_thesaurus = 1

let s:save_cpo = &cpo
set cpo&vim
command! -nargs=1 GetSynonym call thesaurus#get_synonym(<f-args>)
let &cpo = s:save_cpo
unlet s:save_cpo
