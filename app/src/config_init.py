import json

from .scraper import Scraper
from .parser import Parser
from .csv_writer import CSVWriter
from .db_writer import DBWriter


class Config(object):
    def __init__(self, cfg_path: str, file_name: str):
        with open(cfg_path) as json_file:
            cfg = json.load(json_file)

        self.URL = cfg['url']
        self.scraper = Scraper(cfg['scraper'])
        self.parser = Parser(cfg['parser'])
        # self.writer = CSVWriter(cfg['writer'], file_name)
        self.writer = DBWriter(cfg['writer'])


    def get(self):
        representation = {
                'URL': self.URL,
                'scraper': self.scraper,
                'parser': self.parser,
                'writer': self.writer,
        } 

        return representation

