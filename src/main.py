import json
import time
from bs4 import BeautifulSoup

from scraper import Scraper
from parser import Parser
from writer import Writer
from config_init import Config


def save(cfg: dict, page_number: int):
    '''Scrapes, parses and writes data from HTML page into file.
        Arguments:
            cfg (dict): Configurations for custom classes.
            page_number (int): Number of web-page.
    '''
    URL = cfg['URL']
    scraper = cfg['scraper']
    parser = cfg['parser']
    writer = cfg['writer']
    max_page_count = cfg['max_page_count']
    current_page_url = URL + f'&p={page_number}'

    try:
        for count, offer in enumerate(scraper.scrape_page(current_page_url)):
            writer.save_to_file(parser.parse_offer(offer[0]))

    # WAF rate limit error exception.
    except TypeError as type_error:
        print('Error while scraping\nSleeping...') 
        print(type_error)
        time.sleep(60)

        return page_number

    # Internet connection error.
    except ConnectionResetError as con_error:
        print('Connection Error')
        raise con_error

    return page_number + 1


def main():
    cfg_path = '../configs/config.json' 
    file_name = '../output/test_data' 
    max_page_count = 54

    cfg = Config(cfg_path, file_name, max_page_count).get()

    page_stop = 1 # To start iteration.

    while True:
        if (page_stop != 0) and (page_stop != max_page_count):
            page_stop = save(cfg, page_stop)
        else:
            break


if __name__ == "__main__":
    main()

