# MtG Card Rater

Magic : The Gathering is a constantly expanding game, with many functional redos (or reprints) of their previously printed cards. It is often hard to discern whether a ‘newer version’ of a card is strictly better, and with the flurry of releases it can even be difficult to see if a newer version has been made. With many instances of these functionally identical cards it can be difficult to assess manually which of them is the optimal choice for a deck, and so this app was designed to streamline this process.

The repository in its current state is far from complete, as I had to postpone work on this project.

## How it works

### Technologies: Python, Django, BeautifulSoup, Requests, Pandas 

The program utilises the ScryFall API to find user queried cards and return their stats, from here there is a crude semantic analysis that utilises the comparison methods from the Pandas library to match their similarity to a collection of phrases that reflect the common indicators of positive qualities of resource accruement such as card and mana advantage. This same mechanism is applied to cards scraped from MtGGoldfish, an aggregator site for top tournament-level magic the gathering decks. 

## Optimisations

The largest bottleneck of the project in terms of runtime was retrieving entries from the extremely large JSON file which contained entries for the 27,000 unique MtGCards that exists. For this reason, restrictions to what would be retrieved were applied, for example eliminating cards that had a cost over 2 orders higher than the queried card. To further reduce the amount of searching and retrieval required, I implemented functionality that only accessed and scraped the URLs of the top 8 decks from MtGGoldfish, then removed any duplicate card entries from the scraped data.

## Potential Features and Plans

As the project is unfinished, whenever the opportunity arises that will be the primary task regarding it. The majority of the work towards that would be packaging the data for the API endpoint defined by the functional API I will create using DRF. From there, I would create a simple React App to allow users to supply queries to the backend, and return a graphical representation of the rating of their queried card, along with some candidates that have a better or comparable score.

A more robust semantic analysis would also increase the quality of the scoring too, and I would use the opportunity to expand my knowledge on machine learning and AI libraries such as PyTorch to assist in this. This would be further complimented by an implementation of a trie, to cut down on the time needed to iterate over the cards’ text.

An additional decklist scraper would also augment the quality of assessment, as different sites aggregate their data from disparate tournament results, and would therefore create a more accurate depiction of what is being played in the highest echelon of the game and assess cards more objectively. 
