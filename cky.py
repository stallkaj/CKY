#!/usr/local/bin/python3 
import sys

def parse_line():
    tList = []
    ntList = []
    for line in sys.stdin:
        if len(line) <= 1:
            break
        line = line.strip('\n') 
        rule = line.split('->')
        lhs = rule[0].strip(' ')
        rhsSides = rule[1].split('|')
        
        
        for rhs in rhsSides:
            rhs = rhs.strip(' ').split(' ')
            if len(rhs) == 1:
                tList.append([lhs, rhs])
            else:
                ntList.append([lhs, rhs]) 
    return tList, ntList


def create_variable_list(ntList):

    variableSet = set()
    for rule in ntList:
        variableSet.add(rule[1][0])
        variableSet.add(rule[1][1])
    return sorted(variableSet)

def parse_sentences():
    sentences = []
    for line in sys.stdin:
        sentences.append(line.strip('\n').split(' '))
    return sentences


def init_p_matrix(tList, ntList, string, variableList):
    p={}
    for j in range(1, len(string)+1):
        for rule in tList:
            if string[j-1] == rule[1][0]:
                p[(1,j,rule[0])] = rule  
    for i in range(2,len(string)+1):
        for j in range(1,len(string)+2 - i):
            for k in range(1, i):
                for rule in ntList:
                    A = rule[0]
                    B = rule[1][0]
                    C = rule[1][1]
                    if p.get((k,j,B)) and p.get((i-k,j+k,C)):
                        p[(i,j,A)] = [rule[0], [(k,j,B),(i-k,j+k,C)]]
                        
    return p                    
                    
def print_tree(node, p):
    stepChild = p.get(node)
    if len(stepChild[1]) == 1:
        treeString = ' (' + stepChild[0] + ' ' + stepChild[1][0] + ')'
        return treeString
    leftChild = stepChild[1][0]
    rightChild = stepChild[1][1]
    parent = stepChild[0]
    treeString = ' (' + parent +' '
    treeString += print_tree(leftChild, p)
    treeString += print_tree(rightChild, p)
    return treeString + ')'
    

tList, ntList = parse_line()
strings = parse_sentences()
variableList = create_variable_list(ntList)
print('tList:', tList)
print('ntList:', ntList)
print('strings', strings)
print('variableList:', variableList)
for string in strings:
    p = init_p_matrix(tList, ntList, string, variableList)
    #print(p)
    print(string,': ')
    root = p.get((len(string),1,'S'))
    if not root:
        print('0 parse trees')
        continue
    treeString = print_tree((len(string),1,'S'), p)
    print(treeString)
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
