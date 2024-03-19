import requests 
import time
from bs4 import BeautifulSoup 


class Scraper(object):
    def __init__(self, config: dict):
        self.cfg = config

    def scrape_page(self, url: str) -> list:
        '''Scrape all offer pages from selected page.
            Arguments:
                url (str): URL of main page.
            Returns:
                _ (list): List of scraped offer pages (soup objects).
        '''
        try:
            links = self._get_links(url)
            
            return [(self._extract_offer(link), link) for link in links]
            
        except Exception as e:
            print('Faced errors during links scraping')
            raise e

    def _get_links(self, url: str) -> list:
        '''Get links of offer pages from main page.
            Returns:
                _ (list): List of strings - URLs of offer pages. 
        '''
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html5lib')
        links = soup.find_all(self.cfg['tag'], self.cfg['attr'])
        
        return { link.find('a', href=True)['href'] for link in links }

    @staticmethod
    def _extract_offer(link):
        '''Scrape everything from offer page.
            Arguments:
                link (str): URL of offer page.
            Returns:
                soup (bs4.BeautifulSoup): Scraped offers results.
        '''
        offer = requests.get(link)
        soup = BeautifulSoup(offer.content, 'html5lib')
        time.sleep(5) # To avoid IP ban.

        return soup

