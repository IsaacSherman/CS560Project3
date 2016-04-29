import pickle


def loadTitleFile(filename='simplewiki-20160305-all-titles'):
    retlist = []
    retdict = {}
    count = 0
    with open(filename, 'r', encoding='utf8') as fin:
        for line in fin.readlines():
            modded = replaceSpecialStartingTokens(line)
            retdict[modded] = count
            retlist.append(modded)
            count += 1
    return retdict, retlist


def findBetween(longText, begin, end, ignoreTrailingSymbols=False):
    ret = []
    start = 0
    while (1):
        start = longText.find(begin, start) + len(begin)
        if start == len(begin) - 1:
            break
        last = longText.find(end, start)
        if last == -1:
            if not ignoreTrailingSymbols:
                ret.append(longText[start:])  # found the open token, not the close.
            break
        ret.append(longText[start:last])
    return ret


def parseFile(contents, tokens, ret):
    # Take a chunk of text, break it into blocks (more or less a more structured version of split
    for token in tokens:
        ret[tokens['open']] = findBetween(contents, tokens['open'], tokens['close'])
    return ret


def turnIntoTokenStruct(openToken, closeToken):
    return {'open': openToken, 'close': closeToken}


def testAux():
    longText = "This is a long sentence<!> with <b>random</b> tags in <i>it which don't make much" \
               " sense but </i> will at least illustrate <?> how <b>the function</b> should be used <!>"
    openTokens = ["<b>", "<i>", '<a >', '<?>', 'a', ' ']
    closeTokens = ["</b>", "</i>", '< u>', '<!>', 'i', ' ']
    tokens = []
    for i in range(0, len(openTokens)):
        tokens.append(turnIntoTokenStruct(openTokens[i], closeTokens[i]))

    tokenDict = {}
    for token in tokens:
        tokenDict = parseFile(longText, token, tokenDict)

    for token in tokens:
        print("Token " + token['open'] + ": ", tokenDict[token['open']])


def preprocesslevel1(filename="simplewiki-20160305-pages-meta-current.xml"):
    openTokens = ["<title>", '<text xml:space']
    closeTokens = ["</title>", '</text>']
    tokens = []
    for i in range(0, len(openTokens)):
        tokens.append(turnIntoTokenStruct(openTokens[i], closeTokens[i]))

    with open("superStripped.txt", 'w', encoding='utf8') as fout:
        with open(filename, 'r', encoding='utf8') as file:
            on = False
            for line in file.readlines():
                for token in tokens:
                    if token['open'] in line:
                        on = True
                        fout.write(line)
                    elif token['close'] in line:
                        on = False
                        fout.write(line)
                if on:
                    start = line.find('[[')
                    end = line.find(']]')
                    if (start > -1):
                        fout.write(line[start:])


def replaceSpecialStartingTokens(item):
    listOfInvalidTokens = [
        'User_talk:',
        'Wikipedia:',
        'Category:',
        'Talk:',
        'User:',
        'Help:',
        'Wikipedia_talk:',
        'Template:',
        'Template_talk:',
        'MediaWiki:',
        "MediaWiki_talk:",
        'Category_talk:',
        'Help_talk:',
        'File:',
        "Module:",
        "Module_talk:",
        "EVILHORSE:"

    ]
    item = item.replace("&quot;", '"')
    item = item.replace("&amp;", "&")
    item = item.replace("&gt;", ">")
    item = item.replace("&lt;", "<")
    item = item.replace("{", "")
    item = item.replace("#", "")
    item = item.replace("[", "")
    item = item.strip(",\t \r\n#")

    if item.find(":") != -1:
        for token in listOfInvalidTokens:
            if item.find(token) == 0:
                item = item.replace(token, "")
    return item.strip(',')


def preprocessLevel2(file='superStripped.txt'):
    tokens = []
    delim = "!!!|!!!"
    tokenDict = {}
    tokens.append(turnIntoTokenStruct('[[', ']]'))
    with open(file, 'r', encoding='utf8') as fin:
        with open('minimal.txt', 'w', encoding='utf8') as fout:
            for line in fin.readlines():
                if '<title>' in line:
                    start = line.find('<title>') + 7
                    end = line.find('</title>')
                    fout.write(line[start:end] + delim)
                    tokenDict = {}

                for token in tokens:
                    tokenDict = parseFile(line, token, tokenDict)
                for item in tokenDict[tokens[0]['open']]:
                    if "File:" in item:
                        continue
                    item = item.replace(' ', '_')
                    item = item.replace("\n", "")
                    item = replaceSpecialStartingTokens(item)
                    end = item.find('|')
                    if end == -1:
                        end = len(item.strip())
                    fout.write(item[0:end])
                    fout.write(', ')
                if '</text>' in line:
                    fout.write('\n')
                    tokenDict = {}




def intifyDicts():
    global intDict

    intDict = {}

    def intifyList(strlist, dict):
        ret = set()
        for string in strlist:
            if string not in dict:
                continue
            ret.add(dict[string])
        ret = list(ret)
        ret.sort()
        return ret



    for key in titleDict.keys():
        if key not in linkDict:
            linkDict[key] = []#Dangler
        intDict[titleDict[key]] = intifyList(linkDict[key], titleDict)
    return intDict

def preprocessLevel3(filename='minimal.txt'):
    ret = {}
    delim = "!!!|!!!"
    with open(filename, 'r', encoding='utf8') as fin:
        for line in fin.readlines():
            line = line.strip()
            while line.find(delim) != line.rfind(delim):
                print("Stripping delim from line:", line)
                start = line.find(delim)
                line = line[0:start + len(delim)] + line[start + len(delim):].replace(delim, '')
            if delim not in line:
                print("delim Not found", line)
                continue
            title, linkstr = line.split(delim)
            title = title.replace(" ", "_")
            title = replaceSpecialStartingTokens(title)
            links = linkstr.split(', ')
            if title in ret.keys():
                print("duplicate title found:", title)
            else:
                ret[title] = set()

            for link in links:
                if (link in ret[title]):
                    pass
                else:
                    ret[title].add(link)
    return ret



#preprocesslevel1()
#preprocessLevel2()
try:
    linkDict = pickle.load(open('linkDict.pkl', 'rb'))
except IOError:
    linkDict = preprocessLevel3()
    pickle.dump(linkDict, open('linkDict.pkl', 'wb'))

global titleDict, titleList

titleDict, titleList = loadTitleFile()
titleKeys = set()
for key in titleDict.keys():
    titleKeys.add(key)
linkKeys = set()
for key in linkDict.keys():
    linkKeys.add(key)

fusedSet = titleKeys.union(linkKeys)
linkKeys = list(linkKeys)
linkKeys.sort()
titleKeys = list(titleKeys)
titleKeys.sort()

fusedSet = list(fusedSet)
fusedSet.sort()
titleDict = {}
fusedArray = []
for i in range(0, len(fusedSet)):
    titleDict[fusedSet[i]] = i
    fusedArray.append(fusedSet[i])
    i+=1


with open('titleListSorted.txt', 'w', encoding='utf8') as fout:
    for key in titleKeys:
        fout.write(key + "\n")
with open('linkListSorted.txt', 'w', encoding='utf8') as fout:
    for key in linkKeys:
        fout.write(key + "\n")

print("Dumped sorted lists")

titleKeys = None
linkKeys = None

try:
    intDict = pickle.load(open('intDict.pkl','rb'))
except IOError:
    intDict = intifyDicts()
    pickle.dump(intDict, open('intDict.pkl', 'wb'))

with open('titleLen.txt', 'w') as lenFile:
    lenFile.write(str(len(fusedSet)))

defaultVal = 1.0/len(fusedSet)

with open("dataFile", 'w') as fout:
    for key in intDict:
        fout.write(str(key) + ","+str(defaultVal)+"|:")
        tempstr = ""
        for num in intDict[key]:
            tempstr += str(num)
            tempstr+=","
        tempstr= tempstr[0:len(tempstr)-1]
        fout.write(tempstr+"\n")




# https://gist.github.com/diogojc/1338222
