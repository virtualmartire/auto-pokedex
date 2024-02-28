# ❤️🖤🤍 auto-pokedex ❤️🖤🤍

These are the codes and data of the project told in https://medium.com/@virtualmartire/i-built-an-algorithm-that-finds-the-optimal-pokemon-team-01ea152824a9.

## algorithms

paldea.py is the script used to collect the datasets/paldea.csv data. Basically it uses BeautifulSoup to scan serebii.net and get all the relevant info.

## datasets

paldea.csv is the pokedex for the Paldea region (of Pokemon Scarlet & Violet), collected with the paldea.py script cited above. It comprises pokemon names, numbers, types and base stats.

In the attackdex folder you can find the single-pokemon learnable attacks data instead.

## to fix:
- in a few entry of the attackdex, some TMs are referred to the various forms of the relative pokemon...
- pokemon with multiple types combination can bring to ambiguous conclusions

## bibliography
- main data source: https://serebii.net/
- weaknesses table: https://github.com/zonination/pokemon-chart/blob/master/chart.csv
- types HEX colors: https://gist.github.com/apaleslimghost/0d25ec801ca4fc43317bcff298af43c3
- pokemon images: https://pokemondb.net