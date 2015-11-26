#!/usr/local/bin/python3 
import sys

def parse_line():
    grammarList = []
    for line in sys.stdin:
        if len(line) <= 1:
            break
        line = line.strip('\n') 
        rule = line.split('->')
        lhs = rule[0].strip(' ')
        rhsSides = rule[1].split('|')
        
        
        for rhs in rhsSides:
            rhs = rhs.strip(' ').split(' ')
            rule = {'lhs': lhs}
            if len(rhs) == 1:
                rule['Term'] = rhs[0]
            else:
                rule['Prod'] = rhs

         
        grammarList.append(rule)
    return grammarList


def parse_sentences():
    sentences = []
    for line in sys.stdin:
        sentences.append(line.strip('\n').split(' '))
    return sentences


#init_p_matrix():
    
    
print(parse_line(), parse_sentences())
