from .logger import Logger
from .url_pages import URLPages
from bs4 import BeautifulSoup as BS
import re

class WikipediaTableParser:
    def __init__(self):
        self.ROOT_URL = 'https://en.wikipedia.org'
        self.sleep_time = 5
        self.parser = 'html5lib'
        self.urls = set()

    def set_parser(parser: str):
        self.parser = parser

    def set_sleep(sleep_time: int):
        self.sleep_time = sleep_time

    def _wikipedia_table_parser(self, soup_obj):
        '''
        This is a custom parser to get all the tables from a wikipedia page.
        From each table, the goal is to get all references. The references follow the pattern:
        - /wiki/.* : other wiki pages. Build the url as {WIKIPEDIA_ROOT_LINK}{<match>}
        - #cite : citations in the same wiki. Need to search the {current_page}<citation> and get the href of it
        - #CITE : same as #cite
        - http[s]?://<url> common url
        - //<url> : same as putting http[s]?://<url>. This case needs to add the http
        '''
        references_url = set()
        invalid_urls_regex = r'.*(Wikipedia:|Talk:)'

        for soup_obj_table in soup_obj.find_all('table', attrs={'class': 'wikitable'}):
            soup_obj_with_href = soup_obj_table.find_all(href=True)

            for href in soup_obj_with_href:
                href = href.get('href')

                # Filter invalid urls
                href = href.split('#')[0] # Get only the first url slice if the link is <url>#session
                if re.match(invalid_urls_regex, href):
                    continue

                # Match possibilities
                if re.match(r'^/wiki/.*', href):
                    references_url.add(f'{self.ROOT_URL}{href}')
                elif re.match(r'^#(cite|CITE).*', href):
                    new_url = f'{page_url}{href}'
                elif re.match(r'^//.*', href):
                    references_url.add(f'https:{href}')
                elif re.match(r'^https?.*', href):
                    references_url.add(href)

        return references_url

    def add_url(self, urls):
        self.urls.update(urls)

    def run(self):
        page_references = dict()

        for url in self.urls:
            html = URLPages.get_html(url)
            soup_obj = BS(html, self.parser)
            page_references[url] = self._wikipedia_table_parser(soup_obj)


        return page_references
