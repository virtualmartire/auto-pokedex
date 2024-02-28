import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

#
##
### Get the URLs of all the Pokémon in the Paldea Pokédex
##
#

# Send HTTP request
response = requests.get('https://serebii.net/pokedex-sv/')

# Parse the content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the 'form' tag with the name "galar" (wrong documentation...)
form = soup.find('form', attrs={'name': 'galar'})

# Collect all the interesting URLs
select_tag = form.find('select')
urls_list = []
for option in select_tag.find_all('option'):
    # Get the value of the 'value' attribute
    value = option.get('value')
    urls_list.append(value)
urls_list.pop(0)

#
##
### Scan every Pokémon page to get their stats and moves
##
#

pokedex = []

for pokedex_index, pokemon_url in enumerate(urls_list):

    pokedex_entry = {}
    pokemon_attackdex = []

    response = requests.get(f"https://serebii.net/{pokemon_url}")
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', attrs={'class': 'dextable'})

    # Name
    info_table = tables[1]
    second_row = info_table.find_all('tr')[1]
    data_cells = second_row.findChildren('td', recursive=False)
    pokedex_entry['name'] = data_cells[0].text

    # Types
    types_box = data_cells[-1]
    types_variants_rows = types_box.find_all('tr')
    if len(types_variants_rows) > 0:
        types_variants = {}
        for row in types_variants_rows:
            variant = row.find_all('td')[0].text
            types_list = row.find_all('td')[1].find_all('a')
            type_1 = types_list[0].get('href')[12:-6]
            type_2 = types_list[1].get('href')[12:-6] if len(types_list) > 1 else None
            types_variants[variant] = [type_1, type_2]
        if "Paldean" in types_variants.keys():
            pokedex_entry['type_1'] = types_variants["Paldean"][0]
            pokedex_entry['type_2'] = types_variants["Paldean"][1]
        elif "Normal" in types_variants.keys():
            pokedex_entry['type_1'] = types_variants["Normal"][0]
            pokedex_entry['type_2'] = types_variants["Normal"][1]
        else:
            random_int = random.randint(0, len(types_variants.keys())-1)
            random_key = list(types_variants.keys())[random_int]
            pokedex_entry['type_1'] = types_variants[random_key][0]
            pokedex_entry['type_2'] = types_variants[random_key][1]
    else:
        types_list = types_box.find_all('a')
        pokedex_entry['type_1'] = types_list[0].get('href')[12:-6]
        pokedex_entry['type_2'] = types_list[1].get('href')[12:-6] if len(types_list) > 1 else None

    # Stats
    stats_table = tables[-1]
    third_row = stats_table.find_all('tr')[2]
    data_cells = third_row.find_all('td')
    pokedex_entry['base_hp'] = int(data_cells[1].text)
    pokedex_entry['base_atk'] = int(data_cells[2].text)
    pokedex_entry['base_def'] = int(data_cells[3].text)
    pokedex_entry['base_sp_atk'] = int(data_cells[4].text)
    pokedex_entry['base_sp_def'] = int(data_cells[5].text)
    pokedex_entry['base_speed'] = int(data_cells[6].text)

    # Level-up moves
    a_hook = soup.find_all('a', attrs={'name': 'attacks'})[0]
    attacks_tables = a_hook.find_all_next('table', attrs={'class': 'dextable'})
    level_attack_table = attacks_tables[0]
    level_attack_table_rows = level_attack_table.find_all('tr')
    level_attack_table_rows.pop(0)
    level_attack_table_rows.pop(0)
    for i in range(0, len(level_attack_table_rows), 2):
        row = level_attack_table_rows[i]
        data_cells = row.find_all('td')
        level = data_cells[0].text
        attack_name = data_cells[1].a.text
        attack_type = data_cells[2].img.get('src').split('/')[-1].split('.')[0]
        category = data_cells[3].img.get('src').split('/')[-1].split('.')[0]
        try:
            power = int(data_cells[4].text)
        except:
            power = data_cells[4].text
        accuracy = int(data_cells[5].text)
        pp = int(data_cells[6].text)
        pokemon_attackdex.append({
            'name': attack_name,
            'source': f"lv. {level}" if level != '—' else 'nature',
            'type': attack_type,
            'category': category,
            'power': power,
            'accuracy': accuracy,
            'pp': pp
        })

    # TM moves
    for attack_table in attacks_tables:
        attack_table_rows = attack_table.findChildren('tr', recursive=False)
        title_row = attack_table_rows.pop(0)
        if title_row.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])[0].text == 'Technical Machine Attacks':
            tm_attack_table_rows = attack_table_rows[1:]
            for i in range(0, len(tm_attack_table_rows), 2):
                row = tm_attack_table_rows[i]
                data_cells = row.find_all('td')
                tm_number = data_cells[0].a.text
                attack_name = data_cells[1].a.text
                attack_type = data_cells[2].img.get('src').split('/')[-1].split('.')[0]
                category = data_cells[3].img.get('src').split('/')[-1].split('.')[0]
                try:
                    power = int(data_cells[4].text)
                except:
                    power = data_cells[4].text
                accuracy = int(data_cells[5].text)
                pp = int(data_cells[6].text)
                pokemon_attackdex.append({
                    'name': attack_name,
                    'source': tm_number,
                    'type': attack_type,
                    'category': category,
                    'power': power,
                    'accuracy': accuracy,
                    'pp': pp
                })
            break

    print(pokedex_index+1)
    print("Stats:")
    print(pokedex_entry)
    print("Attacks:")
    print(pokemon_attackdex[0])
    print("[...]")
    print(pokemon_attackdex[-1])
    print()

    # Save the attackdex
    pd.DataFrame(pokemon_attackdex).to_csv(f"datasets/attackdex/paldea/{pokedex_entry['name']}.csv", index=False)

    # Save the pokedex entry and checkpoint the pokedex
    pokedex.append(pokedex_entry)
    pd.DataFrame(pokedex).to_csv("datasets/paldea.csv", index=False)