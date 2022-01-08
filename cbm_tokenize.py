#!/usr/bin/env python3

import re
import sys

# TODO - this bug, leave things in quotes alone
#   500 print "{ clr }"



# keywords from here:
# (1) petcat -k2 | tr -d '\n' | sed 's/\s/ /g'
# (2) then manually edit and escape: ',' '+' '*' '$' 
# (3) apparently "go" is a keyword bug, remove from list
# (4) Also, they are inconsistant with keywords that take (), remove '('

tokens = "end for next data input# input dim read let goto run if restore gosub return rem stop on wait load save verify def poke print# print cont list clr cmd sys open close get new tab to fn spc then not step \+ - \* / ^ and or > = < sgn int abs usr fre pos sqr rnd log exp cos sin tan atn peek len str\$ val asc chr\$ left\$ right\$ mid\$".split()

# And I like to have no spaces in these keywords with () required:
no_spaces = "asc atn chr\$ cos exp fre int left\$ len log mid\$ peek right\$ rnd sgn sin spc sqr str\$ tab tan usr val".split()

# TODO - make command line option
# Don't put spaces around operators (my preference)
no_operators = "\+ - \* / ^ > = <".split()

tokens = set(tokens) - set(no_spaces) - set(no_operators)

token_regex = "("
for x in tokens:
    token_regex += x
    token_regex += "|"

# Make quotes "stuff" it's own token
#token_regex += ('".+?"|')  # Doesn't match ""
token_regex += ('".*"|')
# Add ":" as a token - and add closing ')' to regex
token_regex += (":)")


for line in sys.stdin:
    tokenized = re.split(token_regex, line.strip())
    # print(tokenized)
    for tok in tokenized:
        tok = tok.strip()
        # hack to make a comparison operator followed by a
        #  token have no spaces. This happens to just be:
        #  <comparison>"string", all other combos are
        #  nonsense.
        if re.match('.*=$|.*<>$|.*<$|.*>$', tok):
            # I like a="", not a= ""
            print("{}".format(tok),end='')
            continue
        if tok != '':
            print("{} ".format(tok),end='')
            pass
    print("")
