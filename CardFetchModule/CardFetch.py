import json
with open(r'C:\Users\teddy\PycharmProjects\MtGCardRater\assets\oracle-cards.json', encoding='utf-8') as f:
    oracle_card = json.load(f)

query = "Path to Exile"

card_dict = {}

card_index = [item["name"] for item in oracle_card]
card_index = sorted(card_index)


def card_search(str, dictionary):
    card_dict_keys = ['mana cost', 'cmc', 'type_line', 'oracle_text', 'power', 'toughness', 'colors', 'color_identity',
                      'keywords', 'image_uris']
    for item in oracle_card:
        if item["name"] == str:
            dictionary.update({item["name"]: {key: value for key, value in item.items() if key in card_dict_keys}})

def spell_check(str):
    candidates = []
    for card in card_index:
        if card == str:
            return str
            break
        else:
            card_split = list(card)
            char_match = 0
            for char in list(str):
                if char == card_split[char_match] and char_match != len(card_split) - 1:
                    char_match += 1
            if char_match + 2 >= len(str) <= char_match - 2:
                candidates.append(card)
    print(len(candidates))





