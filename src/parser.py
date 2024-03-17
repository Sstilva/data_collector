from bs4 import BeautifulSoup


class Parser(object):
    def __init__(self, config: dict):
        self.cfg = config

    def parse_offer(self, offer: BeautifulSoup) -> dict:
        '''Extracts data from raw scraped HTML offer.
            Arguments:
                offer (bs4.BeautifulSoup): scraped offer.
            Returns:
                processed_offer (dict): ordered dictionary with named parsed offer parts.
        '''

        processed_offer = dict()

        title = lambda x: x[0].split(', ')
        address = lambda x: ''.join(x).split(', ')[:-1]
        under = lambda x: dict(zip(*[iter(x)]*2))
        factoids = under
        desc = lambda x: x[0].replace('\n', ' ')
        summary = lambda x: dict(zip(*[iter(x[1:])]*2))
        price = lambda x: x[0].replace('\xa0', '').replace('₽', '')
        seller = lambda x: dict({x[0]: x[1]})

        process_part = {
                "title": title,
                "address": address,
                "underground": under,
                "factoids": factoids,
                "desc": desc,
                "summary": summary,
                "price": price,
                "builder-premium": seller, 
                "builder": seller, 
                "agent": seller,
                "agency": seller,
        }

        for key, raw_part in zip(process_part.keys(), self._extract_raw(offer)):
            clean_part = []

            if raw_part:
                try:
                    text = raw_part.find_all(text=True)
                    clean_part = process_part[key](text)
                except Exception as e:
                    print(e)

            processed_offer[f'{key}'] = clean_part

        return processed_offer

    def _extract_raw(self, offer: BeautifulSoup):
        '''Extracts raw data from offer using given config with HTML tags.
            Arguments:
                offer (bs4.BeautifulSoup): offer HTML page.
            Return:
                part (generator): iterates over parts of offer by HTML tags.
        '''
        for part in self.cfg.keys():
            part = offer.find(self.cfg[part]['tag'], self.cfg[part]['attr'])
            yield part

