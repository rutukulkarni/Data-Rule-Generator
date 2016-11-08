 # Apriori

class ItemSet:
    def __init__(self):
        self.listItem = []
        self.supCount = 0
        self.confidence = 0
        self.isFreq = 0
        self.isClosedFreq = True
        self.isMaximalFreq = True

class Rule:
    def __init__(self):
        self.left = []
        self.right = []
        self.confidence = 0


dataList = []
itemCount = dict()
possibleKVals = 0
itemDict = dict()
distColList = dict()
listOfPossCols = []

# INPUT DATA

threshold = 7
method = 1
minConfidence = 0.5
evaluationType = 2
filename = 'nursery.data'


def findItemSetSupCount(listItemset):
    tempSupCount = 0
    itemSetLen = len(listItemset)
    itemObjs = itemDict[itemSetLen]
    for itemObj in itemObjs:
        if itemObj.listItem == listItemset:
            tempSupCount = itemObj.supCount
    return tempSupCount

def displayRule(rule):
    ruleLeftList = []
    for item in range(len(rule.left)):
        ruleLeftList =  str(item)
    return ruleLeftList

def generateRules():

    print 'Generating rules....'
    rule = Rule()
    ruleList = []
    conf = 0
    for itemType in range(1,len(itemDict)):
        itemObjs = itemDict[itemType]
        if not len(itemObjs) == 0 and len(itemObjs[0].listItem) > 2:
            for itemObj in itemObjs:
                for itemIndex in range(1,len(itemObj.listItem)):
                    conf = 0
                    listLeft = itemObj.listItem[:itemIndex]
                    listRight = itemObj.listItem[itemIndex:]
                    leftSupCnt = 1
                    rightSupCnt = 1
                    leftSupCnt = findItemSetSupCount(listLeft)
                    rightSupCnt = findItemSetSupCount(listRight)
                    if leftSupCnt > 0:
                        if evaluationType == 1: #conf based pruning
                            conf = float(itemObj.supCount)/float(leftSupCnt)
                        if evaluationType == 2 : #lift based
                            conf1 = float(itemObj.supCount)/(float(leftSupCnt))
                            conf = float(conf1) / (float(rightSupCnt)/float(len(dataList)))

                    if conf > minConfidence:
                        rule.left = listLeft
                        rule.right = listRight
                        rule.confidence = conf

                        print retrieveItemSet(listLeft), '--> ', retrieveItemSet(listRight)
                    ruleList.append(rule)

def generateColList(distColList):
    colList = []
    for colKey in distColList:
        colList = distColList.get(colKey)
        for col in colList:
            listOfPossCols.append(col)


def retrieveItemSet(itemList):
    decodedList = []
    for item in itemList :
        decodedList.append(listOfPossCols[item])
    return decodedList

def getCount(dataMatrix,itemSet):
    list = itemSet.listItem
    itemSet.supCount = 0
    for i in range(len(dataMatrix)):
        count1 = 0
        for j in list:
            if dataMatrix[i][j] == 1:
                count1 = count1 + 1
        if count1 == len(list) and count1 != 0:
            itemSet.supCount += 1



def generateFOneKminus1ItemSet(dataMatrix):

    print 'Generating frequent item-sets....'
    itemSetList = []
    totalItemSets = 0
    possibleKVals = len(dataList[0])
    k = 1

    # GENERATING INITIAL ITEM-SET 1

    for j in range (len(dataMatrix[0])-1):
        x = ItemSet()
        count = 0
        for i in range(len(dataMatrix)-1):
            if dataMatrix[i][j] == 1:
                count = count + 1

        if count > threshold:
            x.isFreq = 1
            x.supCount = count
            x.listItem.append(j)
            itemSetList.append(x)

    itemDict[1] = itemSetList

    #GENERATING 1+ ITEM-SETS

    for i in range(2,possibleKVals):
        itemDict[i] = []
        if len(itemDict[i-1]) > 0:
            for j in itemDict[i-1]:
                for k in itemDict[1]:
                    x = ItemSet()
                    listA = list(j.listItem)
                    listB = k.listItem[0]
                    if listA[len(listA) - 1] < listB:
                        listA.append(listB)
                        totalItemSets+=1
                        x.listItem = listA
                        getCount(dataMatrix,x)
                        percentSupCount = float(x.supCount)/len(dataList)
                        percentThreshold = float(threshold) / 100

                        if percentSupCount > percentThreshold:

                            j.isMaximalFreq = False
                            k.isMaximalFreq = False

                            itemDict[i].append(x)

                            if j.supCount == x.supCount:
                                j.isClosedFreq = False

                            if k.supCount == x.supCount:
                                k.isClosedFreq = False

    print 'done F: (1,K-1) with total itemsets ', totalItemSets

def findCounts(itemDict):

    maximalCount = 0
    closedCount = 0
    freqCount = 0

    for itemType in range(1,len(itemDict)):
        itemObjs = itemDict[itemType]
        for itemObj in itemObjs:
            freqCount+=1
            if itemObj.isClosedFreq == True:
                closedCount+=1
            if itemObj.isMaximalFreq == True:
                maximalCount+=1

    print 'freq count: ', freqCount
    print 'closed count:', closedCount
    print 'maximal  count:',maximalCount

def generateKMinusOneItemSets(dataMatrix):

    print 'Generating frequent item-sets....'
    itemSetList = []
    possibleKVals = len(dataList[0])
    k = 1
    totalItemSets = 0
    # GENERATING INITIAL ITEM-SET 1

    for j in range (len(dataMatrix[0])-1):
        x = ItemSet()
        count = 0
        for i in range(len(dataMatrix)-1):
            if dataMatrix[i][j] == 1:
                count = count + 1

        if count > threshold:
            x.isFreq = 1
            x.supCount = count
            x.listItem.append(j)
            itemSetList.append(x)
        totalItemSets+=1
    itemDict[1] = itemSetList

    #GENERATING 1+ ITEM-SETS
    i = 0

    for i in range(2,possibleKVals):
        itemDict[i] = []
        if len(itemDict[i-1]) > 0:
            for j in itemDict[i-1]:
                for k in itemDict[i-1]:
                    y = ItemSet()
                    listA = list(j.listItem)
                    listB = list(k.listItem)
                    lastEleA = listA[len(listA)-1]
                    lastEleB = listB[len(listB)-1]

                    if len(listA) == len(listB):
                        isValidIS = False
                        l = len(listA)-2
                        if l<=0:
                            l = 1
                        for m in range(l):
                            if listA[m] == listB[m]:
                                isValidIS = True
                        if isValidIS == True or len(listA)==1:
                            if listA[len(listA)-1]>listB[len(listB)-1]:
                                listB.append(lastEleA)
                                totalItemSets+=1
                                y.listItem = listB
                                #print retrieveItemSet(y.listItem)

                        getCount(dataMatrix,y)
                        percentSupCount = float(y.supCount)/len(dataList)
                        percentThreshold = float(threshold) / 100
                        if percentSupCount > percentThreshold:
                            j.isMaximalFreq = False
                            k.isMaximalFreq = False

                            itemDict[i].append(y)

                            if j.supCount == x.supCount:
                                j.isClosedFreq = False
                            if k.supCount == x.supCount:
                                k.isClosedFreq = False

    print 'done F: (K-1,K-1) with total itemsets', totalItemSets

def generateMatrix(noOfTransactions,dataList):

    noOfDistCols = 0
    startColIndex = []
    endColIndex = []
    startColIndex.append(0)
    endColIndex.append(len(distColList[0])-1)
    for i in range(1, len(distColList)):
        startColIndex.append(endColIndex[i-1]+1)
        endColIndex.append(startColIndex[i]+len(distColList[i])-1)
    noOfDistCols= endColIndex[len(endColIndex)-1]+1
    dataMatrix = [[0.0 for x in range(noOfDistCols)] for x in range(noOfTransactions)]

    i = 0
    for i in range(len(dataList)):
        j = 0
        row = dataList[i]
        for j in range(len(row)):
            col = row[j]
            valList = distColList.get(j)
            if valList.index(col)>=0:
                tempIndex = valList.index(col)
                if j == 0:
                    index = tempIndex
                else:
                    index = startColIndex[j]+tempIndex
                dataMatrix[i][index] = 1

    #display(dataMatrix)
    if method == 1:
        generateFOneKminus1ItemSet(dataMatrix)
    if method == 2:
        generateKMinusOneItemSets(dataMatrix)

def display(dataMatrix):
    i=0
    while i< 10:
        print dataMatrix[i]
        i = i+1

def loadData():

    print 'Loading data....'
    global filename

    dataFile = open(filename, 'r')

    noOfTransactions = 0
    ele = []

    for dataLine in dataFile:
        i = 0
        ele = dataLine.split(',')
        noOfTransactions += 1
        ele[len(ele) - 1] = ele[len(ele) - 1].split('\n', 2)[0]

        dataList.append(ele)
        for x in range(len(ele)):
            if distColList.keys().__contains__(x):
                if not ele[x] in distColList[x]:
                    distColList[x].append(ele[x])

                    tempCount = itemCount.get(ele[x])
                    if tempCount is None:
                        itemCount[ele[x]] = 1
                    else:
                        itemCount[ele[x]] = tempCount+1
            else:
                distColList.setdefault(x, []).append(ele[x])
                itemCount[ele[x]] = 1

    #print distColList

    dataFile.close()

    generateColList(distColList)
    generateMatrix(noOfTransactions,dataList)


loadData()
findCounts(itemDict)

generateRules()