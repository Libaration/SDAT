import json


class Config:
    def __init__(self):
        try:
            with open('config.json') as config_file:
                self.config = json.load(config_file)
                self.county = self.config['county']
                self.search_method = self.config['search_method']
                self.submit_button = self.config['submit_button']
                self.steet_number = self.config['street_number']
                self.street_name = self.config['street_name']
                self.second_page_submit_button = self.config['second_page_submit_button']
                self.final_content_container = self.config['final_content_container']
                self.container_data = self.config['container_data']
        except:
            print("Error loading config.json")
            print("Exiting script....")
            exit()
