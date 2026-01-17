import json
from unidecode import unidecode
import json
from pprint import pprint

class ModDisplayLogic():
    def __init__(self):  
        self.liked_mods = []
        self.disliked_mods = []
        self.all_mods_dict = self.get_all_mods_dict()
        
        self.update_current_mod()

    def update_current_mod(self):
        """
        Updates the current mod by iterating through the list of all mods in self.all_mods_dict.
        If that mod is found in l4d2_liked_mods.txt or l4d2_disliked_mods.txt, it is skipped.
        This repeats until a mod is found that is in neither of those files.
        That mod is made the current mod.
        """
        likes_file_dict = self.get_file_dict("l4d2_liked_mods")
        dislikes_file_dict = self.get_file_dict("l4d2_disliked_mods")
        maybe_file_dict = self.get_file_dict("l4d2_maybe_mods")

        for mod_title in self.all_mods_dict:
            if mod_title not in likes_file_dict and mod_title not in dislikes_file_dict and mod_title not in maybe_file_dict:
                self.current_mod = mod_title
                return
        
        # Will raise an exception if there are no more mods left to display. 
        # Meaning that all mods have been seen and no or yes have been pressed for them.
        # raise Exception("There are no more mods left.") 
        self.current_mod = self.get_maybe_mods()
        if self.current_mod == None:
            self.current_mod = "placeholder"
    
    def get_maybe_mods(self):
        """
        Is only called when all mods have been filtered.
        Is used to get the current mod when only maybe mods are left.
        """
        maybe_file_dict = self.get_file_dict("l4d2_maybe_mods")
        
        for mod_title in maybe_file_dict:
            return mod_title

    def remove_maybe_mod(self):
        maybe_file_dict = self.get_file_dict("l4d2_maybe_mods")

        if self.current_mod in maybe_file_dict:
            maybe_file_dict.pop(self.current_mod)
            maybe_file_json = json.dumps(maybe_file_dict, indent=2)

            with open("l4d2_campaign_selector/filtered_mods/l4d2_maybe_mods.json", "w", encoding="utf-8") as maybe_file:
                maybe_file.write(maybe_file_json)

    def get_all_mods_dict(self):
        """Converts all mods from JSON to a Python dictionary"""
        with open("l4d2_campaign_selector/left_4_dead_2_scraper/l4d2_mods.json", "r", encoding="utf-8") as file:
            file_contents = file.read()
            all_mods_dict = json.loads(file_contents)

        return all_mods_dict

    def yes_button_clicked(self):
        """Calls a method to add the current mod to l4d2_liked_mods.json."""
        self.add_current_mod_to_liked()
        self.remove_maybe_mod()

    def no_button_clicked(self):
        """Calls a method to add the current mod to l4d2_disliked_mods.json."""
        self.add_current_mod_to_disliked()
        self.remove_maybe_mod()

    def maybe_button_clicked(self):
        """Calls methods to remove the current mod from l4d2_maybe_mods.json, if possible, and add the current mod to l4d2_maybe_mods.json."""
        # Checks if the current mod is already in the json file.
        # If yes, then it is removed from the json file and added back.
        # Because the current mod is always the one at the top of the JSON file, moving it to the bottom means the current mod changes.
        # If the current mod was not removed and added back, the maybe button would only be able to be clicked once for each mod.
        # Meaning that upon looping through the maybe mods again after all other mods have been filtered, 
        # it would get stuck on the first maybe mod at the top of the JSON file and not update.
        maybe_file_dict = self.get_file_dict("l4d2_maybe_mods")
        if self.current_mod in maybe_file_dict:
            self.remove_maybe_mod()

        self.add_current_mod_to_maybe()

    def add_current_mod_to_file(self, file_name):
        with open(f"l4d2_campaign_selector/filtered_mods/{file_name}.json", "r+", encoding="utf-8") as file:
            file_contents = file.read()

            if file_contents == "":
                file.write(json.dumps({}, indent=2))
                file.seek(0)  # Moves cursor to start from beginning of file rather than the end, which is blank.
                file_contents = file.read()   # Rereads the file for the new contents.
            
            file_dict = json.loads(file_contents)
            file_json = self.format_file_entry(file_dict)
            file.seek(0)  # Reset cursor to beginning of file.
            file.write(file_json)

    def add_current_mod_to_liked(self):
        """Adds the current mod to l4d2_liked_mods.json."""
        self.add_current_mod_to_file("l4d2_liked_mods")

    def add_current_mod_to_disliked(self):
        """Adds the current mod to l4d2_disliked_mods.json."""
        self.add_current_mod_to_file("l4d2_disliked_mods")

    def add_current_mod_to_maybe(self): 
        self.add_current_mod_to_file("l4d2_maybe_mods")

    def format_file_entry(self, file_dict: dict) -> json:
        """
        Adds the current mod to the specified file_dict (liked, disliked, maybe).
        
        :param file_dict: A dictionary of l4d2 mods from one of the mod files.
        :return: Returns a json object that contains all l4d2 mods of the specified file_dict (liked, disliked, maybe).
        :rtype: json
        """
        current_mod_details = self.get_current_mod_details()
        mod_title = current_mod_details[0]
        mod_thumbnail = current_mod_details[1]
        mod_rating = current_mod_details[2]
        mod_url = current_mod_details[3]
        mod_description = current_mod_details[4]

        file_dict[mod_title] = {}
        file_dict[mod_title]["mod_thumbnail"] = mod_thumbnail
        file_dict[mod_title]["mod_rating"] = mod_rating
        file_dict[mod_title]["mod_url"] = mod_url
        file_dict[mod_title]["mod_description"] = mod_description
        
        file_json = json.dumps(file_dict, indent=2)
        return file_json

    def get_current_mod_details(self):
        """Returns a tuple where each element relates to a specific detail about the current mod."""
        mod_title = self.current_mod
        mod_thumbnail = self.all_mods_dict[mod_title]["mod_thumbnail"]
        mod_rating = self.all_mods_dict[mod_title]["mod_rating"]
        mod_url = self.all_mods_dict[mod_title]["mod_url"]

        # Gets the mod description and translates unicode escape sequences into readable text.
        mod_description = self.all_mods_dict[mod_title]["mod_description"]
        mod_description = mod_description.encode("utf-8")
        mod_description = mod_description.decode("unicode-escape")
        
        return mod_title, mod_thumbnail, mod_rating, mod_url, mod_description
    
    def get_total_number_of_mods(self):
        """Returns the total number of mods."""
        return len(self.get_all_mods_dict())

    def get_number_of_mods_left(self):
        """Returns the number of mods left."""
        total_number_of_mods = self.get_total_number_of_mods()
        
        # Maybe mods are not counted as seen as they are served back to the user later.
        number_of_mods_seen = 0
        number_of_mods_seen += self.get_file_dict_length("l4d2_liked_mods")
        number_of_mods_seen += self.get_file_dict_length("l4d2_disliked_mods")

        number_of_mods_left = total_number_of_mods - number_of_mods_seen
        return number_of_mods_left

    def get_file_dict_length(self, file_name):
        with open(f"l4d2_campaign_selector/filtered_mods/{file_name}.json", "r", encoding="utf-8") as file:
            file_contents = file.read()
            
            if file_contents == "":
                file_dict_length = 0
            else:
                file_dict = json.loads(file_contents)
                file_dict_length = len(file_dict)

        return file_dict_length
    
    def get_file_dict(self, file_name):
        with open(f"l4d2_campaign_selector/filtered_mods\{file_name}.json", "r", encoding="utf-8") as file:
            file_contents = file.read()
            if file_contents != "":
                file_dict = json.loads(file_contents)
            elif file_contents == "":
                file_dict = {}

        return file_dict

if __name__ == "__main__":
    x = ModDisplayLogic()
    x.get_number_of_mods_left()
    # print(x.get_current_mod_details())
