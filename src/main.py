import json

from scraper import Scraper
from parser import Parser


def main():
    with open('config.json') as json_file:
        cfg = json.load(json_file)

    URL = cfg['url']

    scraper = Scraper(cfg['scraper'])
    parser = Parser(cfg['parser'])


    max_page_count = 2 # Change to try-except to scrape max possible.

    for page in range(1, max_page_count):
        current_page_url = URL + f'&p={page}'
        for offer in scraper.scrape_page(current_page_url):
            # print(offer.prettify())
            parser.parse_offer(offer)

            break


if __name__ == "__main__":
    main()

