import json

from scraper import Scraper
from parser import Parser
from writer import Writer


def main():
    with open('config.json') as json_file:
        cfg = json.load(json_file)

    URL = cfg['url']
    file_name = "test_data"
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

            'Type of Housing', 'Bathroom',
            'Ceilings', 'Balcony/Loggia',
            'Windows View', 'Renovation',
            'Construction Series', 'Elevators Count',
            'Construction Type', 'Flooring type',
            'Parking', 'Entrances',
            'Heating', 'Building AR',

            'Price',

            'Builder-Premium', 'Builder',
            'Agent', 'Agency'
    ]

    scraper = Scraper(cfg['scraper'])
    parser = Parser(cfg['parser'])
    writer = Writer(file_header, file_name)

    max_page_count = 54 # 54

    for page in range(1, max_page_count):
        current_page_url = URL + f'&p={page}'
        print(f"Page number: {page}")

        for count, offer in enumerate(scraper.scrape_page(current_page_url)):
            # writer.save_to_file(parser.parse_offer(offer[0]))
            print("o")

            # for key, value in parser.parse_offer(offer[0]).items():
            #     print(f'{key}:\n{value}\n')


if __name__ == "__main__":
    main()

