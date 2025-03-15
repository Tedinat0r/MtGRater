import pandas as pd

import CardFetchModule.CardFetch

card_dict = {}


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
    return terms


class Card:
    def __init__(self, dictionary, superdict):
        self.name = superdict.keys()[superdict.keys().index()]
        self.cmc = dictionary['cmc']
        self.effect = fragment(dictionary['oracle_text'])
        self.score = ''


class CardAssessor:
    def __init__(self):
        self.resource_matrix = ['Add one mana','Add {G}', 'Add {W}',
                                                                              'Add {R}', 'Add {B}', 'Add {U}',
                                                                              'Create a treasure',
                                                                              'library for a basic land'
                                                                              'card and put it onto the battlefield',
                                                                              'Search your library for a land card and '
                                                                              'put it onto the battlefield',
                                                                              f'Gain {int} life', f'Pay {int} life',
                                                                              "Return it to its owner's hand",
                                                                              'Put it on the top of ', 'Tap target',
                                                                              'Put it on the bottom of',
                                                                              f'Exile {int} cards from your',
                                                                              "Exile a card from your opponent's "
                                                                              "graveyard"]
        self.card_advantage_matrix = pd.DataFrame({'positive':['draw x cards', 'draw a card', 'draw a card for each',
                                                               'draw cards equal to', 'return target card from your graveyard',
                                                               'return target permanent', 'return target instant or sorcery',
                                                               'return target historic', 'create a token', 'create a token for',
                                                               'reveal cards until', 'search your library for a card', 'search your library for an',
                                                               'search library for a card with']})


    def frag2index_parse(self, index, oracle_text):
        new_index = []
        for term in index:
            if len(new_index) > 0:
                new_index += [element if element.find(term) != -1 else oracle_text.remove(element)for element in oracle_text]
            else:
                new_index = [element if element.find(term) != -1 else oracle_text.remove(element) for element in
                              oracle_text]
        return new_index

    def index_assemble(self, ot):
        return self.frag2index_parse(self.card_advantage_matrix, ot) + self.frag2index_parse(self.resource_matrix, ot)

    def comp_df_assemble(self, index, candidates, dictionary):
        comp_index = []
        comp_scores = []
        tc = candidates[0]
        candidates.pop(0)
        for card in candidates:
            card_score = [1 if element == any in index else 0 for element in fragment(dictionary[card]["oracle_text"])]
            assessment_df = pd.DataFrame(columns={'positive': card_score}, index=index)
            comp_index.append(card)
            comp_scores.append(assessment_df["positive"].sum())
        tc_score = sum([1 if element == any in index else 0 for element in fragment(dictionary[tc]["oracle_text"])])
        comp_df = pd.DataFrame(columns={'score': comp_scores}, index=comp_index)
        return comp_df, tc_score

    def return_candidates(self, df, tc_score):
        final_candidates = []
        df.sort_values(by=["score"], ascending=False)
        while len(final_candidates) != 3:
            for item in df.index:
                print(item)
                if df.loc[item, 'score'] >= tc_score:
                    final_candidates.append(item)
        return final_candidates