# -*- coding: utf-8 -*-

#from lib.dictionaries.dictionary import Dictionary
import requests
from bs4 import BeautifulSoup
import re 

class TaishaneseDict():
    def __init__(self):
        self.url = "https://www.stephen-li.com/TaishaneseVocabulary/MySQLSearch.php"
    def _search(self, data) -> list[str]:
        r = requests.post(self.url, data)
        r.encoding = 'utf-8'
        html = r.text.split("<hr>")
        soups = [BeautifulSoup(h, "lxml") for h in html]
        results = []
        if len(soups) > 0:
            result = soups[0].get_text("\n", strip=True)
            result = result.split("\n")
            result = result[2:]
            results.append(result)
        for soup in soups[1:]:
            result = soup.get_text("\n", strip=True)
            result = result.split("\n")
            results.append(result)
        entries=[]
        
        for result in results:
            if len(result) < 7:
                continue
            curr = 0
            while curr < len(result):
                word_taishan = result[curr]
                curr +=2
                ipa = result[curr]
                curr += 2
                if result[curr] == 'mandarin:':
                    canto = ''
                    curr += 1
                else:
                    canto = result[curr]
                    curr += 2
                if result[curr] == 'english:':
                    mando = ''
                    curr += 1
                else:
                    mando = result[curr]
                    curr += 2
                if curr < len(result):
                    definition = result[curr]
                    curr += 1
                    while curr < len(result):
                        definition += '. ' + result[curr]
                        curr +=1
                    else:
                        pass
                else:
                    pass
                entry = f'**{word_taishan}**({ipa})\n ' \
                    f'  Mandarin: {mando}\n'\
                    f'  Cantonese: {canto}\n\n'\
                    f'  Definition: {definition}\n'\
                    '__________'
                entries.append(entry)
        return entries
    def search_taishanese(self, query):
        data = {
            "data": query,
            "Select1": "Taishanese",
            "Select2": "Partial"
        }
        return self._search(data)
    def search_cantonese(self, query):
        data = {
            "data": query,
            "Select1": "Cantonese",
            "Select2": "Partial"
        }
        return self._search(data)
    def search_mandarin(self, query):
        data = {
            "data": query,
            "Select1": "Mandarin",
            "Select2": "Partial"
        }
        return self._search(data)
    def search_english(self, query):
        data = {
            "data": query,
            "Select1": "English",
            "Select2": "Partial"            
        }
        return self._search(data)