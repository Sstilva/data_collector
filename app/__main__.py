import json
import time
import argparse
from bs4 import BeautifulSoup

from src import Config


def parse_save(cfg: dict):
    '''Scrapes, parses and writes data from HTML page into file.
        Arguments:
            cfg (dict): Configurations for custom classes.
    '''
    URL = cfg['URL']
    scraper = cfg['scraper']
    parser = cfg['parser']
    writer = cfg['writer']

    num_offers_on_page = 28
    # To start iteration.
    page_number = 1 
    max_page_number = scraper.get_offers_count(URL)

    while True:
        try:
            current_page_url = URL + f'&p={page_number}'
            print(page_number)

            if page_number > max_page_number:
                break

            for offer in scraper.scrape_page(current_page_url):
                writer.save_offer(parser.parse_offer(offer[0]), offer[1])

        # WAF rate limit error exception.
        except TypeError as type_error:
            print('Error while scraping\nSleeping...') 
            print(type_error)
            time.sleep(60)

        # Internet connection error.
        except ConnectionResetError as con_error:
            print('Connection Error')
            raise con_error
        
        else:
            page_number += 1


def main(cfg_path: str):
    file_name = 'output/test_data' 
    cfg = Config(cfg_path, file_name).get()

    parse_save(cfg)


if __name__ == "__main__":

    class Namespace(object):
        pass

    ns = Namespace()
    argparser = argparse.ArgumentParser()
    argparser.add_argument('config_path')
    args = argparser.parse_args(namespace=ns)

    main(ns.config_path)

