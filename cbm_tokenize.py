#!/usr/bin/env python3

import re

program = open("r.v2.bas", 'r');

# keyworks from here:
# https://github.com/DNSGeek/vim-cbmbasic
tokens = "\
abs and asc atn chr$ close \
clr cmd cont cos data def \
dim end exp fn for fre \
get gosub goto if input \
int left len let list \
load log mid new next not \
on open or peek poke pos \
print read restore return \
right rnd run save sgn sin \
spc sqr status st step stop str$ \
sys tab tan then time ti time ti \
to usr val verify wait \
"

tokens = tokens.split()

token_regex = "("
for x in tokens:
    token_regex += x
    token_regex += "|"

token_regex += (":)")  # also add ":" as token

# TODO - leave things in quotes alone

for line in program:
    tokenized = re.split(token_regex, line.strip()) 
    # print(tokenized)
    for tok in tokenized:
        if tok != '':
            print("{} ".format(tok.strip()),end='')
    print("")
