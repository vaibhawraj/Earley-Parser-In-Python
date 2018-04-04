__author__ = "Vaibhaw Raj"

# Grammer Rule
class GrammerRule:
    def __init__(self,clusterSymbol,categories,isTerminal=False):
        self.clusterSymbol = clusterSymbol;
        self.categories = [];
        self.categories.extend(categories);
        self.isTerminal = isTerminal;

    def __repr__(self):
        msg = self.clusterSymbol + " -> "
        cat_l = len(self.categories)
        for i in range(0,cat_l):
            if(i!=0):
                msg = msg + " | "
            orderedList = self.categories[i]
            orderedList_l = len(orderedList)
            for j in range(0,orderedList_l):
                if(j!=0):
                    msg = msg + " "
                msg = msg + orderedList[j]
        return msg

# State
class State:
    def __init__(self,stateSymbol,orderedList,startPosition,dotPosition,dotIndex,addedBy):
        self.stateSymbol = stateSymbol
        self.startPosition = startPosition
        self.dotPosition = dotPosition
        self.dotIndex = dotIndex
        self.orderedList = []
        self.orderedList.extend(orderedList)
        
        self.addedBy = addedBy
        self.parentState = []
        if(len(orderedList) == (dotIndex)):
            self.isComplete = True
        else:
            self.isComplete = False
    
    def __repr__(self):
        msg = self.stateSymbol + ' ' + chr(8594) + ' ';
        orderedList_l = len(self.orderedList)
        for i in range(0,orderedList_l):
            if(i!=0):
                msg = msg + " "
            if(i == (self.dotIndex)):
                msg = msg + " " + chr(8226) + " "
            msg = msg + self.orderedList[i]
        if((self.dotIndex) == orderedList_l):
            msg = msg + " " + chr(8226) + " "
        indent = 7;
        msg_l = len(msg) + 3
        tab_n = int(msg_l/8)
        #msg = msg + ("\t"*(indent-tab_n))
        msg = msg + "[" + str(self.startPosition) + "," + str(self.dotPosition) + "] "
        return msg
