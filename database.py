import json
import random


class Database:
    def __init__(self):
        with open('locations.json', 'r') as fp:
            self.locations = json.load(fp)
        with open('country_codes.json', 'r') as fp:
            self.valid_country_codes = json.load(fp)
        with open('application_ids.json', 'r') as fp:
            self.valid_appids = json.load(fp)

    def get_random_locations(self, number):
        total = len(self.locations)
        if number > total:
            number = total
        random.seed()
        return random.choices(self.locations, k=number)

    def get_random_appid(self):
        random.seed()
        return random.choice(self.valid_appids)

    def get_random_country_code(self):
        random.seed()
        return random.choice(self.valid_country_codes)

    def is_location_valid(self, location):
        if location in self.locations:
            return True
        else:
            return False
