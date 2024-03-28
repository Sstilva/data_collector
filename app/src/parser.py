from bs4 import BeautifulSoup


class Parser(object):
    def __init__(self, config: dict):
        self.cfg = config

    def parse_offer(self, offer: BeautifulSoup) -> list:
        '''Parses data from scraped offer into filtered list.
            Arguments:
                offer (bs4.BeautifulSoup): Scraped HTML offer. 
            Returns:
                filtered (list): List of parsed data separated by tags.
        '''
        title = lambda x: x[0].split(', ')
        address = lambda x: ''.join(x).split(', ')[:-1]
        under = lambda x: dict(zip(*[iter(x)]*2))
        factoids = under
        desc = lambda x: x[0].replace('\n', ' ')
        summary = lambda x: dict(zip(*[iter(x[1:])]*2))
        price = lambda x: x[0].replace('\xa0', '').replace('₽', '')
        seller = lambda x: dict({x[0]: x[1]}) if x != [] else None

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
        filtered = []
        
        for name, tag  in zip(self.cfg, self._extract_tag(offer)):
            if tag:
                filtered.append(process_part[name](tag.find_all(text=True)))
            else:
                filtered.append(None)

        return filtered

    def _extract_tag(self, offer: BeautifulSoup):
        '''Returns selected HTML tag from passed offer.
            Arguments:
                offer (bs4.BeautifulSoup): scraped offer object.
            Returns:
                tag (bs4.element.Tag or None): tag extracted from offer or
                                               None if no tag was found.
        '''
        for name in self.cfg:
            try:
                tag = offer.find(self.cfg[name]['tag'], self.cfg[name]['attr'])
            except AttributeError as e:
                tag = None
            finally:
                yield tag
    
