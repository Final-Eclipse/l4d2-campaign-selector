import json

with open("left_4_dead_2_scraper/l4d2_mods.json", "r") as file:
    file_contents = file.read()
    mod_dict = json.loads(file_contents)

for mod_title in mod_dict:
    print(mod_title)

import json

with open("left_4_dead_2_scraper/l4d2_mods.json", "r") as file:
    file_contents = file.read()
    mods = json.loads(file_contents)

for mod_title, mod_details in mods.items():
    print(mod_title, mod_details)
    print()
    break
