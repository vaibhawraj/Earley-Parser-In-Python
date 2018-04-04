__author__ = "Vaibhaw Raj"

from nltk.stem import PorterStemmer
from DataStructure import GrammerRule
from helper import *
import re

ps = PorterStemmer()

def tokenizer(Input):
    symbols = []
    
    #First Parse split using white space
    results = re.split("([\s])",Input)
    temp = []
    for s in results:
        if not len(s.strip())==0:
            temp.append(s.strip())

    # now if any symbol is not valid decimal, then split it based on any non alphanumeric character
    for s in temp:
        if isDecimal(s):
            symbols.append(s)
        else:
            results = re.split("([^\w\d-])",s)
            for t in results:
                if not len(t.strip())==0:
                    if re.match("^[\w\d]+\-+$",t.strip()):
                        for t_ in t.strip().split('-'):
                            symbols.append(t_.strip())
                    else:
                        symbols.append(t.strip())
    return symbols

def printSummary(lineNo,line):
    tokens = tokenizer(line)
    
    for t in tokens:
        symbolType = '';
        if isString(t):
            symbolType = 'STRING'
        else:
            if isInt(t):
                symbolType = 'INT'
            else:
                if isDecimal(t):
                    symbolType = 'DOUBLE'
                else:
                    symbolType = 'OP'

        if(symbolType == 'STRING'):
            stemmed = ps.stem(t)

            if(stemmed.lower() == t.lower()):
                print(t,symbolType,lineNo)
            else:
                print(t,symbolType,lineNo,stemmed)
        else:
            print(t,symbolType,lineNo)

def inputSentenceTokenizer(w):
    sym = []
    w = " ".join(w.split("=")[1:])
    if w[len(w)-1] == '.':
        w = w[:len(w)-1]
    w_tokens = w.split(' ')
    for t in w_tokens:
        if isDecimal(t):
            sym.append(t)
            continue
        mObj = re.match("^[\w]+\.$",t)
        if mObj:
            sym.append(t)
            continue
        results = re.split("[^\w\d\-\.]",t)
        for t_ in results:
            if not len(t_.strip()) == 0:
                sym.append(t_)
    return sym

def grammerRuleTokenizer(line):
    sym = []
    
    line = line.strip()
    
    #Split colon
    line_colon_split = line.split(":")
    if(len(line_colon_split) != 2):
        print("Error: Parsing Grammer Rule at '" + line + "'")
        exit()
    
    sym.append(line_colon_split[0].strip())
    sym.append(":")
    
    line = line_colon_split[1]
    line_pipe_split = re.split("(\||\ )",line)
    for c in line_pipe_split:
        if(len(c.strip())==0):
            continue
        
        if isDecimal(c):
            sym.append(c)
            continue
        mObj = re.match("^[a-zA-Z-]+\.?$",c)
        if mObj:
            sym.append(c)
            continue
        
        for ct in re.split("([^\w\d])",c):
            ct = ct.strip()
            if(len(ct)==0):
                continue
            sym.append(ct)
    return sym

def generateGrammer(Input):
    split_semicolon = Input.split(';')
    inputSentence = []
    rules = {}
    for line in split_semicolon:
        line = line.strip()
        if(len(line) == 0):
            continue
        if '=' in line and line[0].lower() == 'w':
            inputSentence.extend(inputSentenceTokenizer(line))
        elif ':' in line:
            # Its part of grammer rule
            grToken = grammerRuleTokenizer(line)
            grName = grToken[0]
            if not re.match("^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)?$",grName):
            	print("Error: Expected STRING token as non-terminal symbol but got '" + grName + "' at line '" + line +"'")
            	exit()

            cat = []
            temp = []
            for token in grToken[2:]:
                if(token == '|'):
                    cat.append(temp)
                    temp = []
                else:
                    mObj = re.match("^[a-zA-Z0-9\.-]+$",token)
                    if mObj:
                        temp.append(token)
                    else:
                        print("Error: Unexpected symbol in grammer '" + token + "' line in '" + line + "'")
                        exit()
            if(len(cat)==0):
                cat.append(temp)
            elif not cat[len(cat)-1] == temp:
                cat.append(temp)
            if(grName in rules.keys()):
                rules[grName].categories.extend(cat)
            else:
                rules[grName] = GrammerRule(grName, cat)
        else:
            # Its invalid line
            print("Error: Unable to parse grammer at",line)
            exit()

    if(len(inputSentence) == 0):
        print("Error: Input sentence is missing")
        exit()

    return (inputSentence,rules)