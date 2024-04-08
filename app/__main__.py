import time
import argparse

from src import Config


def parse_arguments():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('-c', '--config', default='configs/generic.json',
                           help='Path of config file.')
    argparser.add_argument('-f', '--filepath',
                           help='Filepath of resulting CSV file.')
    argparser.add_argument('-d', '--database',
                           help='PostgreSQL database config string.')
    argparser.add_argument('-t', '--timepause', type=int, default=10,
                           help='Sleep time after offer is scraped.')
    argparser.add_argument('-T', '--timeout', type=int, default=60,
                           help='Sleep time when caught and blocked.')
    argparser.add_argument('-r', '--range',
                           help='Total area range.')
    argparser.add_argument('-R', '--rooms',
                           help='Number of rooms.')

    args = argparser.parse_args()
    if args.range.find('-') == -1:
        print('''Total area range argument is incorrect.\n
              Range must be in format: "a-b"''')
        return -1

    if len(args.range.split('-')) != 2:
        print('''Total area range argument is incorrect.\n
              Range must be in format: "a-b"''')
        return -1

    # FIXME add more checks.
    # if args.rooms == 0 or args.rooms > 10:
    #     print('''Rooms argument is incorrect.\n
    #           Number of rooms must be in range from 1 to 6 or "Студия"''')
    #     return -1

    return args


def parse_save(cfg: dict, timeout: int):
    '''Scrapes, parses and writes data from HTML page into file.
        Arguments:
            cfg (dict): Configurations for custom classes.
    '''
    url = cfg['URL']
    scraper = cfg['scraper']
    parser = cfg['parser']
    db_writer = cfg['db_writer']
    csv_writer = cfg['csv_writer']

    n_offers_on_page = 28
    # To start iteration.
    page_number = 1 
    max_page_number = int(scraper.get_offers_count(url) / n_offers_on_page) + 1

    while True:
        try:
            current_page_url = url + f'&p={page_number}'

            if page_number > max_page_number:
                break

            for offer, link in scraper.scrape_page(current_page_url):
                if db_writer:
                    db_writer.save_offer(parser.parse_offer(offer), link)
                if csv_writer:
                    csv_writer.save_offer(parser.parse_offer(offer), link)

        # WAF rate limit error exception.
        except TypeError as type_error:
            print('Error while scraping\nSleeping...') 
            print(type_error)
            time.sleep(timeout)

        # Internet connection error.
        except ConnectionResetError as con_error:
            print('Connection Error')
            raise con_error
        
        else:
            page_number += 1


def main(args: argparse.Namespace):
    cfg = Config(args).get()
    parse_save(cfg, args.timeout)


if __name__ == "__main__":
    args = parse_arguments()

    if args != -1:
        main(args)
    else:
        print('Exiting process...')

