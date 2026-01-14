import json
from unidecode import unidecode

# Get current mod

# If yes is clicked, write that mod to a file for liked mods

# If no is clicked, write that mod to a file for disliked mods

# If maybe is clicked, write that mod to a file for maybe mods
class ModDisplayLogic():
    def __init__(self):  
        self.liked_mods = []
        self.disliked_mods = []
        self.all_mods_dict = self.get_all_mods_dict()
        
        self.update_current_mod()

        # self.current_liked_mods = self.get_liked_mods()
        # self.current_disliked_mods = self.get_disliked_mods()

    def update_current_mod(self):
        """
        Updates the current mod by iterating through the list of all mods in self.all_mods_dict.
        If that mod is found in l4d2_liked_mods.txt or l4d2_disliked_mods.txt, it is skipped.
        This repeats until a mod is found that is in neither of those files.
        That mod is made the current mod.
        """
        with open("l4d2_campaign_selector/filtered_mods\l4d2_liked_mods.txt", "r", encoding="utf-8") as likes_file:
            likes_file_contents = likes_file.read()

            with open("l4d2_campaign_selector/filtered_mods\l4d2_disliked_mods.txt", "r", encoding="utf-8") as dislikes_file:
                dislikes_file_contents = dislikes_file.read()

                for mod_title in self.all_mods_dict:
                    if mod_title not in likes_file_contents and mod_title not in dislikes_file_contents:
                        self.current_mod = mod_title
                        return
        
        # Will raise an exception if there are no more mods left to display. 
        # Meaning that all mods have been seen and no or yes have been pressed for them.
        raise Exception("There are no more mods left.") 
        
    def get_all_mods_dict(self):
        """Converts all mods from JSON to a Python dictionary"""
        with open("l4d2_campaign_selector/left_4_dead_2_scraper/l4d2_mods.json", "r", encoding="utf-8") as file:
            file_contents = file.read()
            all_mods_dict = json.loads(file_contents)

        return all_mods_dict

    def yes_button_clicked(self):
        """Calls a method to add the current mod to l4d2_liked_mods.txt."""
        self.add_current_mod_to_liked()

    def no_button_clicked(self):
        """Calls a method to add the current omd to l4d2_disliked_mods.txt."""
        self.add_current_mod_to_disliked()

    def maybe_button_clicked(self):
        pass

    def add_current_mod_to_liked(self):
        """Adds the current mod to l4d2_liked_mods.txt."""
        with open("l4d2_campaign_selector/filtered_mods/l4d2_liked_mods.txt", "r+", encoding="utf-8") as likes_file:
            likes_file.read() # Moves cursor to end of file
            likes_file.write(self.current_mod + "\n")

    def add_current_mod_to_disliked(self):
        """Adds the current mod to l4d2_disliked_mods.txt."""
        with open("l4d2_campaign_selector/filtered_mods/l4d2_disliked_mods.txt", "r+", encoding="utf-8") as dislikes_file:
            dislikes_file.read() # Moves cursor to end of file
            dislikes_file.write(self.current_mod + "\n")

    def get_current_mod_details(self):
        """Returns a tuple where each element relates to a specific detail about the current mod."""
        mod_title = self.current_mod
        mod_thumbnail = self.all_mods_dict[mod_title]["mod_thumbnail"]
        mod_rating = self.all_mods_dict[mod_title]["mod_rating"]
        mod_url = self.all_mods_dict[mod_title]["mod_url"]

        # Gets the mod description and translates unicode escape sequences into readable text
        mod_description = self.all_mods_dict[mod_title]["mod_description"]
        mod_description = mod_description.encode("utf-8")
        mod_description = mod_description.decode("unicode-escape")
        
        return mod_title, mod_thumbnail, mod_rating, mod_url, mod_description

if __name__ == "__main__":
    x = ModDisplayLogic()
    print(x.get_current_mod_details())