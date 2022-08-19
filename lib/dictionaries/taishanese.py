# -*- coding: utf-8 -*-

#from lib.dictionaries.dictionary import Dictionary
import requests
from bs4 import BeautifulSoup

class TaishaneseDict():
    def __init__(self):
        self.url = "https://www.stephen-li.com/TaishaneseVocabulary/MySQLSearch.php"
    def _search(self, data) -> list[str]:
        r = requests.post(self.url, data)
        r.encoding = 'utf-8'
        html = r.text
        soup = BeautifulSoup(html, "lxml")
        result = soup.get_text(separator="\n", strip=True)
        result = result.split("\n")
        result = result[2:]
        entries = []
        curr = 0
        while curr < len(result):
            word_taishan = result[curr]
            ipa = result[curr+2]
            canto = result[curr+4]
            mando = result[curr+6]
            if curr+9 < len(result) and any([ch.isalpha() for ch in result[curr+9]]):
                definition = result[curr+8] + '\n' + result[curr+9]
                curr += 10
            else:
                curr += 9
            entry = f'**{word_taishan}({ipa})**\n ' \
                f'Mandarin: {mando}'\
                f'Cantonese: {canto}'\
                f'Definition: {definition}'
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
d = TaishaneseDict()
print(d.search_mandarin("台山"))