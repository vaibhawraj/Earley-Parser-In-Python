__author__ = "Vaibhaw Raj"

from DataStructure import GrammerRule, State
from nltk.stem import PorterStemmer
ps = PorterStemmer()

def addToChart(s,c):
    if not isStateInChart(s,c):
        c.append(s)
    
def isPartOfSpeech(word,cat,grammer):
    if cat in grammer.keys():
        #If next cat is a non-terminal symbol
        gRule = grammer[cat]
        terminalSymbols = []
        for rightCat in gRule.categories:
            firstSymbol = rightCat[0]
            if not firstSymbol in grammer.keys():
                terminalSymbols.append(ps.stem(firstSymbol.lower()))
        if ps.stem(word.lower()) in terminalSymbols:
            #then it may have "word" as part of symbols in right, in which case it should go to scanner
            #e.g. His daughter plays cricket, His son man playing football
            return True
        else:          
            #or it may not have "word", in which case it would go to predictor
            #e.g. I eat apple,  I am eating apple
            return False
    else:
        #If next cat is a terminal symbol, means cat is part of speech, it may be equal to word or not equal to word
        #Scanner will decide what to do with this state
        return True


def isStateInChart(s,chart):
    stateAlreadyExist = False
    stateStr = str(s)
    for j in range(0,len(chart)):
            existingState = chart[j]
            if(stateStr == str(existingState)):
                stateAlreadyExist=True
                break
    return stateAlreadyExist

def predictor(s,stateNo,grammer,chart):
    orderedList_l = len(s.orderedList)
    #print(stateNo,s,s.addedBy,"Predictor")
    #Todo What if symbol is not in grammer
    lookupCategory = s.orderedList[s.dotIndex]
    if(lookupCategory in grammer.keys()):
        categories = grammer[lookupCategory].categories
        for cat in categories:
            firstSymbol = cat[0]
            if(firstSymbol in grammer.keys()):
                newState = State(lookupCategory,cat,s.dotPosition,s.dotPosition,0,"Predictor")
                newState.parentState.append(stateNo)
                addToChart(newState, chart[s.dotPosition])
    return

def scanner(word,s,stateNo,grammer,chart):
    lookupCategory = s.orderedList[s.dotIndex]
    if lookupCategory in grammer.keys():
        gRule = grammer[lookupCategory]

        for cat in gRule.categories:
            firstSymbol = cat[0]
            if not firstSymbol in grammer.keys() and ps.stem(word.lower()) == ps.stem(firstSymbol.lower()) :
                #Scanner will always scan first word of if next cat has terminal words and its part of speech
                newState = State(lookupCategory, cat, s.dotPosition, s.dotPosition+1, 1, "Scanner")
                newState.parentState.append(stateNo)
                addToChart(newState, chart[newState.dotPosition])
            
    else:
        # Subject : His . son Noun
        if ps.stem(word.lower()) == ps.stem(lookupCategory.lower()):
            newState = State(s.stateSymbol, s.orderedList, s.startPosition, s.dotPosition+1, s.dotIndex+1, "Scanner")
            newState.parentState.append(stateNo)
            addToChart(newState, chart[newState.dotPosition])

def completer(curState,stateNo,chart):
    # Searching for all previous state that ends at current states start Position and expecting current state
    startPosition = curState.startPosition
    catName = curState.stateSymbol
    for oldState in chart[startPosition]:
        if(not oldState.isComplete and oldState.orderedList[oldState.dotIndex] == catName):
            newState = State(oldState.stateSymbol,oldState.orderedList, oldState.startPosition, curState.dotPosition, oldState.dotIndex+1, "Completer")
            newState.parentState.append(stateNo)
            addToChart(newState,chart[newState.dotPosition])
    return

def earleyParser(W,grammer):
    wordLen = len(W)
    
    #Creating Chart of wordLen + 1 size
    chart = []
    for i in range(0,wordLen+1):
        chart.append([])
        
    #Appending Dummy State
    dummyState = State(chr(947),['S'],0,0,0,'Dummy Start State')
    dummyState.parentState.append(-1)
    stateNo = 0
    print("Chart [0]")
    print("S" + str(stateNo),dummyState)
    predictor(dummyState,stateNo,grammer,chart)
    stateNo = stateNo + 1
    
    parsedSuccessfully = False
    for i in range(0,wordLen+1):
        if(not i==0):
            print("Chart [" + str(i) + "]")
        for s in chart[i]:
            print("S" + str(stateNo),s,s.addedBy)
            if(s.stateSymbol == 'S' and s.startPosition == 0 and s.dotPosition == wordLen):
                parsedSuccessfully = True

            isNextCatPartOfSpeech = False
            if(i<len(W) and not s.isComplete):
                isNextCatPartOfSpeech = isPartOfSpeech(W[i],s.orderedList[s.dotIndex],grammer)
            
            if(not s.isComplete and not isNextCatPartOfSpeech):
                predictor(s,stateNo,grammer,chart)
            elif not s.isComplete and isNextCatPartOfSpeech:
                if(i<len(W)):
                    scanner(W[i],s,stateNo,grammer,chart)
            else:
                completer(s,stateNo,chart)
            stateNo = stateNo + 1
    if parsedSuccessfully == False:
        print("Unable to parse")
    return chart