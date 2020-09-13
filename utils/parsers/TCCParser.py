import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup as BS

from ..file_handler import FileHandler

class TCCParser:
    def __init__(self):
        self._url = None
        self._parser = 'html5lib'

    @property
    def url(self):
        return self._url

    @property
    def parser(self):
        return self._parser

    @url.setter
    def root_url(self, new_url):
        self._url = new_url

    @parser.setter
    def parser(self, new_parser):
        self._parser = new_parser

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
                    references_url.add(self.build_url(href))
                elif re.match(r'^#(cite|CITE).*', href):
                    new_url = f'{page_url}{href}'
                elif re.match(r'^//.*', href):
                    references_url.add(f'https:{href}')
                elif re.match(r'^https?.*', href):
                    references_url.add(href)

        return references_url


    def save_pages(self, page_references):
        for url in page_references:
            file_name = url.split('/')[~0].strip()
            FileHandler.write_tables_csv(file_name, './csvs', page_references[url])

    def build_url(self, path):
        url_parse = urlparse(self._url)
        base_url = f'https://{url_parse.netloc}'

        return f'{base_url}{path}'

    def run(self, html):
        page_references = dict()

        soup_obj = BS(html, self.parser)
        page_references[self._url] = self._wikipedia_table_parser(soup_obj)

        self.save_pages(page_references)

        # This parser doesn't want to read more urls inside this website
        return set()
