import json

from .scraper import Scraper
from .parser import Parser
from .csv_writer import CSVWriter
from .db_writer import DBWriter


class Config(object):
    def __init__(self, args):
        with open(args.config) as json_file:
            cfg = json.load(json_file)

        self.url = self._url_constructor(args.range, args.rooms)
        self.scraper = Scraper(cfg['scraper'], args.timepause)
        self.parser = Parser(cfg['parser'])

        self.db_writer = DBWriter(cfg['writer']) if args.database else None
        self.csv_writer = CSVWriter(cfg['writer']) if args.filepath else None

    def get(self):
        representation = {
                'URL': self.url,
                'scraper': self.scraper,
                'parser': self.parser,
                'db_writer': self.db_writer,
                'csv_writer': self.csv_writer,
        } 

        return representation

    def _url_constructor(self, area_range: str, rooms_num: int) -> str:
        '''Constructs url using input arguments.
            Arguments:
                area_range (str): Range of flat total area in next format "a-b".
                rooms_num (int): Number of flat rooms. 
            Returns:
                _ (str): resulting url with filters applied. 
        '''
        base = 'https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=4777'

        # 9 is code for "Студия" on the website.
        rooms_num = 9 if not rooms_num.isnumeric() else int(rooms_num)
        rooms = f'&room{rooms_num}=1'

        area_range = area_range.split('-')
        mintarea = f'&mintarea={int(area_range[0])}'
        maxtarea = f'&maxtarea={int(area_range[1])}'

        return base + rooms + mintarea + maxtarea

