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


init_p_matrix(grammarList, sentence):
    p={}
    for j in range(len(sentence)):
        for k in range(len(grammarList)):
            if grammarList[k].get('term'):
                p[(1,j,k)] = True  
    for i in range(2,len(sentence)):
        for j in range(1,len(sentence) - i):
            for k in range(1, i):
                for rule in grammarList:
                    if rule.get('prod')
                        
                    
    
print(parse_line(), parse_sentences())





'''
let the input be a string S consisting of n characters: a1 ... an.
let the grammar contain r nonterminal symbols R1 ... Rr.
This grammar contains the subset Rs which is the set of start symbols.
let P[n,n,r] be an array of booleans. Initialize all elements of P to false.
for each i = 1 to n
  for each unit production Rj -> ai
      set P[1,i,j] = true
      
      
  for each i = 2 ti n -- Length of span
    for each j = 1 to n-i+1 -- Start of span
        for each k = 1 to i-1 -- Partition of span
              for each production RA -> RB RC
                      if P[k,j,B] and P[i-k,j+k,C] then set P[i,j,A] = true
                      if any of P[n,1,x] is true (x is iterated over the set s, where s are all the indices for Rs) then
                            S is member of language
                            else
                              S is not member of language
'''
