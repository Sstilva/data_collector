from bs4 import BeautifulSoup


class Parser(object):
    def __init__(self, config: dict):
        self.cfg = config

    def parse_offer(self, offer: BeautifulSoup):
        for raw_part in self._extract_raw(offer):
            if raw_part != None:
                print(raw_part.prettify(), '\n')
            else:
                print(None, '\n')

    # Не использовать cfg clean, перебирать последовательно текст из всех тегов и проверять его?

    def _extract_raw(self, offer: BeautifulSoup):
        '''
        Extracts raw data from offer using given config with HTML tags.
            Arguments:
                offer (bs4.BeautifulSoup): offer HTML page.
            Return:
                part (generator): iterates over parts of offer by HTML tags.
        '''
        for part in self.cfg.keys():
            part = offer.find(self.cfg[part]['tag'], self.cfg[part]['attr'])
            yield part

    def process_raw(self):
        pass

