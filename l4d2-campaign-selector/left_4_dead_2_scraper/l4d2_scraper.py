from bs4 import BeautifulSoup
import requests
from time import sleep, time
from html import unescape
import json
from random import randint
import keyboard

# Will show less mods versus being signed into Steam to hide NSFW 
class Scraper():
    def __init__(self) -> None:
        self.base_url = "https://steamcommunity.com/workshop/browse/?appid=550&requiredtags%5B0%5D=Campaigns&actualsort=trend&p=1"

        base_url_page_index = self.base_url.index("p=") + 2
        starting_page = int(self.base_url[base_url_page_index])
        self.change_page(page_number_to_change_to=starting_page)    # Sets the initial page and scrapes relevant HTML from it

        self.mods = {}
        self.all_descriptions = []

    def execute_scraper(self) -> None:
        """Starts the scraper."""
        start_time = time()
        total_number_of_pages = self.get_total_number_of_pages()

        base_url_page_index = self.base_url.index("p=") + 2
        starting_page = int(self.base_url[base_url_page_index])

        self.current_page = 0

        for page_number in range(starting_page, total_number_of_pages + 1):
            self.change_page(page_number_to_change_to=page_number)

            self.get_mod_details()
            self.get_mod_descriptions()
            self.save_mods_to_text_file()
            self.current_page += 1

            # Spam "esc" to end the scraper early.
            if keyboard.is_pressed("esc"):
                return
            
            # Spam "del" to pause the scraper.
            if keyboard.is_pressed("del"):
                self.pause_scraper()

            # Small input buffer to prevent too many HTTP requests.
            print(f"Page {page_number} out of {total_number_of_pages} completed!")
            print("Spam \"esc\" to end the scraper early.")
            print("Spam \"del\" to pause the scraper.")
            sleep_timer = randint(1, 3)
            print(f"Sleeping for {sleep_timer} seconds.")
            sleep(sleep_timer)
            print(f"Done sleeping for {sleep_timer} seconds.")
            print()
        
        end_time = time()
        print(f"L4D2 Scraper finished in {end_time - start_time}")

    def get_mod_details(self) -> None:
        """Gets the title, thumbnail, rating, and url for every mod on the current page."""
        for mod_panel in self.all_mod_panels:
            mod_title = mod_panel.find("div", class_="workshopItemTitle").text.strip()
            mod_thumbnail = mod_panel.find("img", class_="workshopItemPreviewImage")["src"]
            mod_rating = mod_panel.find("img", class_="fileRating")["src"]  # Image of stars for rating
            mod_url = mod_panel.find("a", class_="ugc")["href"]
            
            self.mods[mod_title] = {
                "mod_thumbnail": mod_thumbnail,
                "mod_rating": mod_rating,
                "mod_url": mod_url
            }
            
    def get_mod_descriptions(self) -> None:
        """Gets all mod descriptions on the current page."""
        all_mod_descriptions_html = self.mod_browsing_page.find_all("script")

        for mod_description in all_mod_descriptions_html:
            mod_description = unescape(str(mod_description))    # Unescape removes HTML entities such as &quot; for double quotes

            # Get starting and ending indexes for index slicing the description
            start_index = mod_description.index('description":"') + len('description":"')
            end_index =  mod_description.index('","user_subscribed')
            mod_description = mod_description[start_index:end_index]

            self.all_descriptions.append(mod_description)

        self.add_mod_descriptions_to_mods(all_descriptions=self.all_descriptions)

    def add_mod_descriptions_to_mods(self, all_descriptions: list) -> None:
        """
        Adds each mod description in all_descriptions to their respective mod in self.mods.
        
        :param all_descriptions: a list containing all mod descriptions
        """
        index = 0
        try:
            for mod_title, mod_details in self.mods.items():
                mod_details["mod_description"] = all_descriptions[index]
                index += 1
        except IndexError:  # Prevents index 30 creating an error. Index 30 does not exist and therefore does not have any mod associated with it.
            pass

    def save_mods_to_text_file(self) -> None:
        """Saves all the mods in self.mods to a text file."""
        # Reads the JSON file and combines any previous entries with the new, current one.
        # Only useful if there are previous entries from prior scraper use.
        with open("l4d2_campaign_selector/left_4_dead_2_scraper/l4d2_mods.json", "r") as file:
            file_contents = file.read()

        file_dict = json.loads(file_contents)
        new_dict = {**file_dict, **self.mods}

        with open("l4d2_campaign_selector/left_4_dead_2_scraper/l4d2_mods.json", "w") as file:
            file.write(json.dumps(new_dict, indent=2))

    def get_total_number_of_pages(self) -> int:
        """Gets the total number of pages available."""
        page_numbers_available_html = self.workshop_browse_paging.find_all("a", "pagelink") # Page numbers shown in the workshop's page control area
        page_numbers_available = []

        for page_number in page_numbers_available_html:
            page_number = int(page_number.text)
            page_numbers_available.append(page_number)

        total_number_of_pages = max(page_numbers_available)
        return total_number_of_pages

    def change_page(self, page_number_to_change_to: int) -> None:
        """
        Changes the current page by modifying self.base_url with the int parameter, page_number_to_change_to. 
        Creates a new requests object and gets the website's html.
        Creates new BeautifulSoup objects based off of the current html.
        
        :param page_number_to_change_to: The page number to change the current url and html to.
        """
        self.base_url = f"https://steamcommunity.com/workshop/browse/?appid=550&requiredtags%5B0%5D=Campaigns&actualsort=trend&p={page_number_to_change_to}"
    
        response = requests.get(self.base_url)
        response_html = response.text

        self.check_status_code(response)

        self.current_page_soup = BeautifulSoup(response_html, "html.parser")    # All HTML

        self.mod_browsing_page = self.current_page_soup.find("div", class_="workshopBrowseItems")   
        self.all_mod_panels = self.mod_browsing_page.find_all("div", class_="workshopItem")   # Mod panel = the squared space that each mod occupies
        self.workshop_browse_paging = self.current_page_soup.find("div", class_="workshopBrowsePaging") # Page control area

    def check_status_code(self, response) -> None:
        """
        Checks the status code of the response and prints an error if any request fails to reach the website.
        
        :param response: A response object that is received after sending a get request to the website.
        """
        if response.status_code != 200: 
            print(f"Failed to reach {self.base_url}.")
            print()
            self.pause_scraper()
        elif response.ok == True:   # Checks if the HTTP request successfully reached the website.
            print(f"Successfully reached {self.base_url}.")

    def get_mod_thumbnail_image_in_bytes(self, mod_thumbnail_url) -> bytes:
        """
        Gets the mod thumbnail image url's content in bytes and returns it.
        
        :param mod_thumbnail_url: The url to the mod's thumbnail image.
        """
        response = requests.get(mod_thumbnail_url)
        response = response.content
        return response
    
    def get_mod_rating_image_in_bytes(self, mod_rating_image_url) -> bytes:
        """
        Gets the mod rating image url's content in bytes and returns it.
        
        :param mod_rating_image_url: The url to the mod's rating image.
        """
        response = requests.get(mod_rating_image_url)
        response = response.content
        return response
    
    def pause_scraper(self):
        is_paused = input("Type \"resume\" to continue scraper. ").lower().strip()
        while is_paused != "resume":
            is_paused = input("Type \"resume\" to continue scraper. ").lower().strip()
    
if __name__ == "__main__":
    l4d2_scraper = Scraper()
    l4d2_scraper.execute_scraper()

    total_number_of_pages = l4d2_scraper.get_total_number_of_pages()
    print(f"Finished scraping {l4d2_scraper.current_page}/{total_number_of_pages} pages.")
