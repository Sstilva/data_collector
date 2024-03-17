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
        for count, offer in enumerate(scraper.scrape_page(current_page_url)):
            # Put another sleep in different place to check if process gets banned.
            print(f"\nOffer number {count}\n{offer[1]}\n")

            for key, value in parser.parse_offer(offer[0]).items():
                print(f'{key}:\n{value}\n')
            # print(offer[0])

            # break


if __name__ == "__main__":
    main()

