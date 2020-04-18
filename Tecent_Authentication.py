import hashlib
import random
from urllib.parse import urlencode

def GetRandomStr(length):
    AlphaFactory = "abcdefghijklmnopqrstuvwxyz"
    str = ""
    for _ in range(length):
        index = random.randint(0, 25)
        str += AlphaFactory[index]
    return str

def GetSign(params, app_key):
    SortDict = sorted(params.items(), key = lambda item: item[0], reverse=False)
    SortDict.append(('app_key', app_key))
    rawtext = urlencode(SortDict).encode()
    sha = hashlib.md5()
    sha.update(rawtext)
    md5text = sha.hexdigest().upper()
    return md5text