" Vim syntaxtax file
" Language: Commodore 64 BASIC V2
" Maintainer: Thomas Knox
" Latest Revision: 21 July 2020

" Revised - burin, 5 January 2022

if exists("b:current_syntax")
    finish
endif

let b:current_syntax = "cbmbasic"

" Keywords
syntax keyword cbmBasicLanguageKeywords abs and asc atn chr$ close
syntax keyword cbmBasicLanguageKeywords ABS AND ASC ATN CHR$ CLOSE

syntax keyword cbmBasicLanguageKeywords clr cmd cont cos data def
syntax keyword cbmBasicLanguageKeywords CLR CMD CONT COS DATA DEF

syntax keyword cbmBasicLanguageKeywords dim end exp fn for fre
syntax keyword cbmBasicLanguageKeywords DIM END EXP FN FOR FRE

syntax keyword cbmBasicLanguageKeywords get gosub goto if input
syntax keyword cbmBasicLanguageKeywords GET GOSUB GOTO IF INPUT

syntax keyword cbmBasicLanguageKeywords int left len let list
syntax keyword cbmBasicLanguageKeywords INT LEFT LEN LET LIST

syntax keyword cbmBasicLanguageKeywords load log mid new next not
syntax keyword cbmBasicLanguageKeywords LOAD LOG MID NEW NEXT NOT

syntax keyword cbmBasicLanguageKeywords on open or peek poke pos
syntax keyword cbmBasicLanguageKeywords ON OPEN OR PEEK POKE POS

syntax keyword cbmBasicLanguageKeywords print read restore return
syntax keyword cbmBasicLanguageKeywords PRINT READ RESTORE RETURN

syntax keyword cbmBasicLanguageKeywords right rnd run save sgn sin
syntax keyword cbmBasicLanguageKeywords RIGHT RND RUN SAVE SGN SIN

syntax keyword cbmBasicLanguageKeywords spc sqr status st step stop str$
syntax keyword cbmBasicLanguageKeywords SPC SQR STATUS ST STEP STOP STR$

syntax keyword cbmBasicLanguageKeywords sys tab tan then time ti time ti
syntax keyword cbmBasicLanguageKeywords SYS TAB TAN THEN TIME TI TIME TI

syntax keyword cbmBasicLanguageKeywords to usr val verify wait
syntax keyword cbmBasicLanguageKeywords TO USR VAL VERIFY WAIT

highlight link cbmBasicLanguageKeywords Keyword

syntax match cbmBasicComment "\vREM.*$"
syntax match cbmBasicComment "\v\#\!.*$"
highlight link cbmBasicComment Comment

syntax match cbmBasicOperator "\v\*"
syntax match cbmBasicOperator "\v/"
syntax match cbmBasicOperator "\v\+"
syntax match cbmBasicOperator "\v-"
syntax match cbmBasicOperator "\v\="
"highlight link cbmBasicOperator Operator

syntax region cbmBasicString start=/\v"/ skip=/\v\\./ end=/\v"/ contains=cbmBasicNonPrintable
"highlight link cbmBasicString type
"highlight link cbmBasicString String

syntax match cbmBasicNumber "\v<\d+>"
syntax match cbmBasicNumber "\v<\d+\.\d+>"
"highlight link cbmBasicNumber Number

syntax region cbmBasicNonPrintable start=/{/ skip=/\v\\./ end=/}/ contained
highlight link cbmBasicNonPrintable preproc

syntax match cbmLineNumber "\v^\s*<\d+>"
highlight link cbmLineNumber Constant
