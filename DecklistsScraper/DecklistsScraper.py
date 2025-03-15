from typing import Iterable

import requests
from bs4 import BeautifulSoup
import CardFetchModule
import json

res = requests.get("https://www.mtggoldfish.com/metagame/legacy#paper")
soup_data = BeautifulSoup(res.text, 'html.parser')
tags = soup_data.find("div", {"class": "deck-display"}).find("div", {"id": "metagame-decks-container"})


def format_scrape(List):
    n = len(List) - 1
    i = 0
    while i <= n:
        string = str(List[i])
        yield string
        i += 1


decks = format_scrape(list(tags.find_all("span", {"class": "deck-price-paper"})))


def deck_names(generator, string):
    deck_cards = []
    for name in generator:
        deck_name = name
        deck_name = str(deck_name).split(">")
        deck_name = str(deck_name[2]).split("<")
        deck_name = str(deck_name[0])
        deck_name = deck_name.strip()
        deck_name = deck_name.replace("!", "")
        deck_name = deck_name.replace("-", " ")
        deck_name = deck_name.replace("'", " ")
        deck_name = deck_name.replace(" ", "-")
        deck_name = deck_name.strip()
        deck_list_request = requests.get(f"https://www.mtggoldfish.com/archetype/{string}-{deck_name}#paper")
        deck_list = BeautifulSoup(deck_list_request.text, "html.parser")
        try:
            #deck_list.find("table", {"class": "deck-view-deck-table"}).find_all("a")
            deck_list.find("div", {"class": "deck-table-buttons-container"}).find_all("a").find("table", {
                "class": "deck-view-deck-table"}.find_all("a"))
            #deck_list.find("div", {"class": "deck-table-buttons-container"}).find_all("a")
            print(list(deck_list.find("div", {"class": "deck-table-buttons-container"}).find_all("a").find("table",{"class": "deck-view-deck-table"}.find_all("a"))))
        except AttributeError:
            print("The URL has inconsistent formatting")
            break
        for word in list(deck_list.find("div", {"class": "deck-table-buttons-container"}).find_all("a").find("table",{"class": "deck-view-deck-table"}.find_all("a"))):
            card = str(word)
            card = card.split(">")
            card = (card[1].split("<"))
            card = card[0]
            deck_cards.append(card)
    return deck_cards






