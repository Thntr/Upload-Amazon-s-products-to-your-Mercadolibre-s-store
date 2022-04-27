import requests
from bs4 import BeautifulSoup

def get_proxy():
    url = "https://github.com/clarketm/proxy-list/blob/master/proxy-list.txt"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    dict = {"https": list(map(lambda x: x[0] + x[1], list(
        zip(map(lambda x: x.text, soup.findAll("td")[::1]), map(lambda x: x.text, soup.findAll("td")[1::1])))))}
    proxyList = dict["https"]

    del proxyList[0:18]
    del proxyList[-3::]

    for i in range(0, len(proxyList) - 1):

        theIndexOfTheGap = str(proxyList[i]).find(" ")
        theStringProxy = str(proxyList[i])
        lengthOfTheStringProxy = len(theStringProxy)
        charactersToErase = lengthOfTheStringProxy - theIndexOfTheGap
        newString = theStringProxy.replace(theStringProxy[-charactersToErase::], "")
        proxyList[i] = newString

    return proxyList[1::2]

proxies = get_proxy()

print(len(proxies))