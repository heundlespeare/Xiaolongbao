from bs4 import BeautifulSoup
import requests
import re

leedsURL = 'http://corpus.leeds.ac.uk/cgi-bin/cqp.pl'
def leedsRequest(params):
    paramsDefault = {
        'searchtype': 'conc',
        'contextsize':'50c',
        'terminate':50
    }
    return requests.get(leedsURL, params=paramsDefault|params)
removePattern = re.compile(r'([>\n ])')
def leedsLookup(corpuslist, searchstring):
    r = leedsRequest({'searchstring': searchstring, 'corpuslist': corpuslist})
    soup = BeautifulSoup(r.content, 'html.parser')
    result = "\n".join([re.sub(removePattern, "", tr.get_text()) for tr in soup.find_all('tr')])
    return result
izh = "INTERNET-ZH"
lcmc = "LCMC"
leedsLookup("\"个女\"", lcmc)