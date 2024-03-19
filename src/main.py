import json
import time
from bs4 import BeautifulSoup

from scraper import Scraper
from parser import Parser
from writer import Writer
from config_init import Config


def save(cfg: dict, page_number: int):
    URL = cfg['URL']
    scraper = cfg['scraper']
    parser = cfg['parser']
    writer = cfg['writer']
    max_page_count = cfg['max_page_count']

    current_page_url = URL + f'&p={page_number}'
    print(f"Page number: {page_number}") # Debug purposes.

    try:
        for count, offer in enumerate(scraper.scrape_page(current_page_url)):
            try:
                writer.save_to_file(parser.parse_offer(offer[0]))
            except ConnectionResetError:
                print("Offer error\nSleeping...")
                print(offer[1])
                time.sleep(15)

                return page_number 

    except TypeError as type_error:
        print('Error while scraping main page links\nSleeping...') 
        # print(parser.parse_offer(offer[0]))
        print(type_error)
        time.sleep(15)

        return page_number

    except ConnectionResetError as con_error:
        print('Connection Error')
        raise con_error

    except Exception as e:
        print(e)
        raise e

    return page_number + 1


def main():

    cfg = Config('config.json', 'test_data', 3).get()
    max_page_count = cfg['max_page_count']
    page_stop = 1 # To start iteration.

    while True:
        if (page_stop != 0) and (page_stop != max_page_count):
            page_stop = save(cfg, page_stop)
        else:
            break



if __name__ == "__main__":
    main()

