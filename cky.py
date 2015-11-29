#!/usr/local/bin/python3 
import sys

class pNode():
    def __init__(self, node, counter=0):
        self.nodeList = []
        self.add_node(node)
        self.counter= counter
        self.index = 0
    def len(self):
        return len(self.nodeList)
    def add_node(self,node):
        
        self.nodeList.append(node)
    def get_node(self):
        rv = self.nodeList[self.index]
        if len(self.nodeList) > 1:
            self.index = (self.index + 1) % len(self.nodeList)
        return rv

class Node():
    def __init__(self,name, leftChildAdd=None, rightChildAdd=None, word=None):
        self.name = name
        self.leftChildAdd = leftChildAdd
        self.rightChildAdd = rightChildAdd
        self.word = word


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
                node = Node(rule[0], word=rule[1][0])
                p[(1,j,rule[0])] = pNode(node,counter=1)
    for i in range(2,len(string)+1):
        for j in range(1,len(string)+2 - i):
            for k in range(1, i):
                for rule in ntList:
                    A = rule[0]
                    B = rule[1][0]
                    C = rule[1][1]
                    leftChildAdd = (k,j,B)
                    rightChildAdd = (i-k,j+k,C)
                    if p.get(leftChildAdd) and p.get(rightChildAdd):
                        node = Node(rule[0], leftChildAdd=leftChildAdd, rightChildAdd=rightChildAdd)
                        if not p.get((i,j,A)):
                            p[(i,j,A)] = pNode(node)
                        else:
                            p[(i,j,A)].add_node(node)
                        p[(i,j,A)].counter += p[leftChildAdd].counter * p[rightChildAdd].counter
                        
    return p                    
                    
def print_tree(pAddress, p, dupFlag):
    pnode = p.get(pAddress)
    if not dupFlag and pnode.len() > 1:
        dupFlag = True
        #p[node] = p[node][1:]
    node = pnode.get_node()
    if node.word:
        return ' (' + node.name + ' ' + node.word + ')', dupFlag
    leftTemp, dupFlag = print_tree(node.leftChildAdd, p, dupFlag)
    rightTemp, dupFlag = print_tree(node.rightChildAdd, p, dupFlag)
    return ' (' + node.name + leftTemp + rightTemp + ')', dupFlag
    

tList, ntList = parse_line()
strings = parse_sentences()
variableList = create_variable_list(ntList)
#print('tList:', tList)
#print('ntList:', ntList)
#print('strings', strings)
#print('variableList:', variableList)
firstLine = True
for string in strings:
    if not firstLine:
        print()
    firstLine = False
    p = init_p_matrix(tList, ntList, string, variableList)
    outputString = ' '.join(string) + ': '
    root = p.get((len(string),1,'S'))
    if not root:
        outputString += '0 parse trees'
    else:
        if root.counter == 1:
            outputString += '1 parse tree'
        else:
            outputString += str(root.counter) + ' parse trees'
        dupFlag = True
        #while dupFlag:
        dupFlag = False
        tempString, dupFlag = print_tree((len(string),1,'S'), p, dupFlag)
        outputString += '\n' + tempString[1:]

        if root.counter > 1:
            tempString, dupFlag = print_tree((len(string),1,'S'), p, dupFlag)
            outputString += '\n' + tempString[1:]
    print(outputString)


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
