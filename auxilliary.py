import numpy as np
import scipy as sp
from numpy import core
from numpy.core import multiarray


def findBetween(longText, begin, end):
    ret = []
    start = 0
    while(1):
        start = longText.find(begin, start) + len(begin)
        if start == len(begin)-1:
            break
        last = longText.find(end, start)
        if last == -1:
            ret.append(longText[start:])#found the open token, not the close.  May want to adjust behavior
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


testAux()

#https://gist.github.com/diogojc/1338222