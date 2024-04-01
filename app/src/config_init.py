import json

from .scraper import Scraper
from .parser import Parser
from .writer import Writer


class Config(object):
    def __init__(self, cfg_path: str, file_name: str, page_count: int):
        with open(cfg_path) as json_file:
            cfg = json.load(json_file)

        self.URL = cfg['url']
        file_header = [
            'Rooms', 'Address', 

            'M_Aviastroitelnaya', 'M_Severny Vokzal',
            'M_Yashlek', 'M_Kozya Sloboda',
            'M_Kremlyovskaya', 'M_Ploshchad Tukaya',
            'M_Sukonnaya Sloboda', 'M_Ametyevo',
            'M_Gorki', 'M_Prospekt Pobedy',
            'M_Dubravnaya',

            'Total Area', 'Living Area',
            'Kitchen Area', 'Floor',
            'Construction Year', 'Completion Year',
            'Building', 'Finishing',

            'Desc',

            'Type of Housing', 'Bathroom',
            'Ceilings', 'Balcony/Loggia',
            'Windows View', 'Renovation',
            'Construction Series', 'Elevators Count',
            'Construction Type', 'Flooring type',
            'Parking', 'Entrances',
            'Heating', 'Building AR',

            'Price',

            'Builder-Premium', 'Builder',
            'Agent', 'Agency',

            'URL'
        ]

        self.scraper = Scraper(cfg['scraper'])
        self.parser = Parser(cfg['parser'])
        self.writer = CSVWriter(cfg['writer'], file_header, file_name)

        self.max_page_count = page_count

    def get(self):
        representation = {
                'URL': self.URL,
                'scraper': self.scraper,
                'parser': self.parser,
                'writer': self.writer,
                'max_page_count': self.max_page_count,
        } 

        return representation

