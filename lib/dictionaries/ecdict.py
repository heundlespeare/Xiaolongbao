#A parser for the CC-Cedict. Convert the Chinese-English dictionary into a list of python dictionaries with "traditional","simplified", "pinyin", and "english" keys.

#Make sure that the cedict_ts.u8 file is in the same folder as this file, and that the name matches the file name on line 13.

#Before starting, open the CEDICT text file and delete the copyright information at the top. Otherwise the program will try to parse it and you will get an error message.

#Characters that are commonly used as surnames have two entries in CC-CEDICT. This program will remove the surname entry if there is another entry for the character. If you want to include the surnames, simply delete lines 59 and 60.

#This code was written by Franki Allegra in February 2020.

#open CEDICT file
import os
from whoosh.fields import Schema, TEXT
from whoosh import index
from whoosh.qparser import QueryParser
from tqdm import tqdm
script_dir = os.path.dirname(__file__)


class ECDict():
    def __init__(self):
        schema = Schema(traditional=TEXT(stored=True), simplified=TEXT(stored=True), pinyin=TEXT(stored=True), english=TEXT(stored=True))
        if not os.path.exists(os.path.join(script_dir, 'cedict_index')):
            index_path = os.path.join(script_dir, 'cedict_index')
            os.mkdir(index_path)
            ix = index.create_in(index_path, schema)
            ix = index.open_dir(index_path)
            writer = ix.writer()
        else:
            ix = index.open_dir(os.path.join(script_dir, 'cedict_index'))
            self._searcher = ix.searcher()
            return
            #idk do something
        with open(os.path.join(script_dir, 'cedict_ts.u8'), 'r', encoding='utf-8') as file:
            print("cock")
            text = file.read()
            lines = text.split('\n')
            dict_lines = list(lines)

        #define functions

            def parse_line(line):
                parsed = {}
                if line == '':
                    dict_lines.remove(line)
                    return 0
                line = line.rstrip('/')
                line = line.split('/')
                if len(line) <= 1:
                    return 0
                english = line[1:]
                char_and_pinyin = line[0].split('[')
                characters = char_and_pinyin[0]
                characters = characters.split()
                traditional = characters[0]
                simplified = characters[1]
                # force all pinyin to be lowercase.
                pinyin = char_and_pinyin[1].lower()
                pinyin = pinyin.rstrip()
                pinyin = pinyin.rstrip("]")
                parsed['traditional'] = traditional
                parsed['simplified'] = simplified
                parsed['pinyin'] = pinyin
                parsed['english'] = "\n".join(english)
                writer.add_document(**parsed)
            '''
            def remove_surnames():
                for x in range(len(list_of_dicts)-1, -1, -1):
                    if "surname " in list_of_dicts[x]['english']:
                        if list_of_dicts[x]['traditional'] == list_of_dicts[x+1]['traditional']:
                            list_of_dicts.pop(x)
            '''        
        #make each line into a dictionary
        print("Parsing dictionary . . .")
        for line in tqdm(dict_lines[30:]):
            parse_line(line)
        writer.commit()
        self._searcher = ix.searcher()
        self.qp = QueryParser("english", schema=self._searcher.schema)
        #remove entries for surnames from the data (optional):

        #print("Removing Surnames . . .")
        #remove_surnames()


        #If you want to save to a database as JSON objects, create a class Word in the Models file of your Django project:

        # print("Saving to database (this may take a few minutes) . . .")
        # for one_dict in list_of_dicts:
        #     new_word = Word(traditional = one_dict["traditional"], simplified = one_dict["simplified"], english = one_dict["english"], pinyin = one_dict["pinyin"], hsk = one_dict["hsk"])
        #     new_word.save()
        print('Done!')
    def search(self, query) -> list[str]:
        q = self.qp.parse(query)
        results = self._searcher.search(q, limit=50)
        descriptions = []
        for word in results:
            description = f'**{word["simplified"]}/{word["traditional"]}({word["pinyin"]})**\n'
            for i, defn in enumerate(word["english"].split("\n")):
                description +=f'   {i+1}. {defn}\n'
            descriptions.append(description)
        return descriptions