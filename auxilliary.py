
import numpy
import scipy
def findBetween(longText, begin, end):
    ret = []
    start = 0
    while(1):
        start = longText.find(begin, start) + len(begin)
        if start == len(begin)-1:
            break
        last = longText.index(end, start)
        ret.append( longText[start:last])
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
    openTokens = ["<b>", "<i>", '<a >', '<?>']
    closeTokens = ["</b>", "</i>", '< u>', '<!>']
    tokens = []
    for i in range(0, len(openTokens)):
        tokens.append(turnIntoTokenStruct(openTokens[i], closeTokens[i]))

    tokenDict = {}
    for token in tokens:
        tokenDict = parseFile(longText, token, tokenDict)

    for token in tokens:
        print("Token " + token['open'] + ": ", tokenDict[token['open']])


testAux()

#https://gist.github.com/diogojc/1338222