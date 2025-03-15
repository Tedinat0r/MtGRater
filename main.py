import pandas as pd
from CardAssessor import AssessorDataFrames as ad
from CardFetchModule import CardFetch
from DecklistsScraper import DecklistsScraper as ds
import CardAssessor
import json
import requests
from bs4 import BeautifulSoup

with open(r'C:\Users\teddy\PycharmProjects\MtGCardRater\assets\oracle-cards.json', encoding='utf-8') as f:
    oracle_card = json.load(f)
oracle_dict = {key["name"]: key["cmc"] for key in oracle_card}
query = "Path to Exile"

card_dict = {}
comp_oracle = ""

card_index = [[item["name"], item["cmc"]] for item in oracle_card]
card_index = sorted(card_index, reverse=True)

CardFetch.card_search(query, card_dict)


def card_index_cmc_trim(array):
    cmc = card_dict[query]["cmc"]
    filtered_index = filter(lambda x: x[1] <= cmc + 1, array)
    return list(filtered_index)


def card_index_meta_trim():
    formats = ["modern", "legacy"]
    shortlist = set()
    for format in formats:
        res = requests.get(f"https://www.mtggoldfish.com/metagame/{format}#paper")
        soup_data = BeautifulSoup(res.text, 'html.parser')
        tags = soup_data.find("div", {"class": "deck-display"}).find("div", {"id": "metagame-decks-container"})
        decks = ds.format_scrape(list(tags.find_all("span", {"class": "deck-price-paper"})))
        try:
            meta = [ds.deck_names(decks, format) for number in range(8)]
        except TypeError:
            print("The URL may have been formatted incorrectly")

        meta = [item for sublist in meta for item in sublist]
        for item in meta:
            try:
                if not oracle_dict[item] > card_dict[query]["cmc"] + 2:
                    shortlist.add(item)
            except KeyError:
                print("This card may be doublesided or not exist")
    return shortlist


def card_oracle_gen(list):
    x = 0
    while x >= len(list):
        CardFetch.card_search(list[x], card_dict)
        yield card_dict[list[x]]["oracle_text"]
        x += 1


def oracle_gen_to_string(generator):
    text = str(generator)
    return text


def fragment(string):
    terms = [item for item in string.split(".")]
    for item in terms:
        if ',' in item:
            terms.append(item[0:item.find(',')])
            terms.append(item[item.find(',') + 1:len(item)])
            terms.remove(item)
        if item == '':
            terms.remove(item)
    terms = [item.lstrip() for item in terms]
    try:
        terms.remove('')
    except ValueError:
        pass
    return terms


class SemanticAnalyzer:
    def __init__(self, query):
        self.card_dict = card_dict
        self.query = query

    def makedict(self, string):
        fragment_dict = {key: 0 for key in string}
        try:
            fragment_dict.pop('')
        except KeyError:
            pass
        return fragment_dict

    def fragment_comp(self, dictionary):
        candidates = []
        for item in card_index_meta_trim():
            print(dictionary)
            CardFetch.card_search(item, card_dict)
            try:
                for element in self.fragment(card_dict[item]["oracle_text"]):
                    if element in list(dictionary.keys()):
                        dictionary[element] += 1
            except KeyError:
                print("Unable to find oracle text")
            if sum(dictionary.values()) >= len(dictionary.keys()) - 1:
                candidates.append(item)
            dictionary = {key: 0 for key in dictionary.keys()}
        semantic_df = pd.DataFrame(dictionary, index=[0])
        candidates.insert(0, query)
        print(semantic_df), print(candidates)
        return semantic_df, candidates


def cards_to_model(array, array2, model):
    bind = lambda y, x: (y[x[0]], CardFetch.card_search())
    for element in enumerate(dir(model)):
        if element[0] / 3 != float or element[0] == 0:
            model.element[1] = array[element[0]]
            model.enumerate(dir(model))[enumerate(dir(model)).index(element + 1)][1] = bind(array2,  )
            model.enumerate(dir(model))[enumerate(dir(model)).index(element + 2)][1]


def main(card):
    def gen_index(cands):
        df_index = []
        for item in cands:
            ext = ad.CardAssessor().frag2index_parse(ad.CardAssessor().resource_matrix, fragment(card_dict[item]
                                                                                               ["oracle_text"]))
            df_index += ext
        return df_index

    #fragment_comp(.makedict(fragment(card_dict[query]["oracle_text"])))
    query = card
    #Initialises target card in dictionary
    final_candidates = SemanticAnalyzer(query=query)
    final_candidates = final_candidates.fragment_comp(final_candidates.makedict(fragment(card_dict[final_candidates.
                                                                                         query]["oracle_text"])))
    #Reduces candidates down to those who are sufficiently syntactically similar
    final_candidates[1].insert(0, query)
    final_index = gen_index(final_candidates[1])
    df_and_tc = ad.CardAssessor().comp_df_assemble(final_index, final_candidates[1], card_dict)
    to_api = ad.CardAssessor().return_candidates(df_and_tc[0], df_and_tc[1])

#main(query)
card_index_meta_trim()


