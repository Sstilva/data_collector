import requests 
import time
from bs4 import BeautifulSoup 


class Scraper(object):
    def __init__(self, config: dict, timepause: int):
        self.cfg_link = config['link']
        self.cfg_count = config['offer_count']
        self.timepause = timepause

    def scrape_page(self, url: str) -> list:
        '''Scrape all offer pages from selected page.
            Arguments:
                url (str): URL of main page.
            Returns:
                _ (list): List of scraped offer pages (soup objects).
        '''
        try:
            links = self._get_links(url)
            
            return [(self._extract_offer(_), _) for _ in links]
            
        except Exception as e:
            print('Faced errors during links scraping')
            raise e

    def get_offers_count(self, url: str):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html5lib')
        offer_count = soup.find(self.cfg_count['tag'], self.cfg_count['attr'])
        offer_count = int(offer_count.text.split(' ')[1])
        time.sleep(self.timepause) # To avoid IP ban.
        
        return offer_count

    def _get_links(self, url: str) -> list:
        '''Get links of offer pages from main page.
            Returns:
                _ (list): List of strings - URLs of offer pages. 
        '''
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html5lib')
        links = soup.find_all(self.cfg_link['tag'], self.cfg_link['attr'])
        
        return { _.find('a', href=True)['href'] for _ in links }

    def _extract_offer(self, link: str):
        '''Scrape everything from offer page.
            Arguments:
                link (str): URL of offer page.
            Returns:
                soup (bs4.BeautifulSoup): Scraped offers results.
        '''
        offer = requests.get(link)
        soup = BeautifulSoup(offer.content, 'html5lib')
        time.sleep(self.timepause) # To avoid IP ban.

        return soup

