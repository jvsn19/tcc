import re
from urllib import request
from urllib.parse import urlparse
import string

import nltk
from newspaper import Article
from bs4 import BeautifulSoup as BS

from ..kafka import KafkaProducer

nltk.download('punkt')

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
                if re.match(invalid_urls_regex, href):
                    continue

                # Match possibilities
                if re.match(r'^/wiki/.*', href):
                    references_url.add(self.build_url(href))
                elif re.match(r'^#(cite|CITE).*', href):
                    new_soup_obj = soup_obj.find('li', attrs={'id': href[1:]})
                    if new_soup_obj:
                        new_href_obj = new_soup_obj.find('a', attrs={'class': 'external text', 'rel': 'nofollow'})
                        if new_href_obj:
                            references_url.add(new_href_obj.get('href'))
                elif re.match(r'^//.*', href):
                    references_url.add(f'https:{href}')
                elif re.match(r'^https?.*', href):
                    references_url.add(href)

        return references_url

    def clean_str(self, s: str) -> str:
        # Remove punctuation
        s = s.translate(str.maketrans('', '', string.punctuation))
        # Remove linebreakers
        s = re.sub(r'(\n|\r)', '', s)
        # Remove leading and trailing spaces
        s = s.strip()
        return s if s else None

    def article_parse(self, url):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        title = ((article.title))
        full_text = ((article.text))
        meta_description = ((article.meta_description))
        summary = ((article.summary))
        #get the list of keywords
        keywords = article.keywords
        aux1 = ''

        for word in keywords:
            aux1 = aux1 +" "+word
        keywords = aux1

        #get the meta keywords
        meta_keywords = article.meta_keywords
        aux2 = ''

        for word in meta_keywords:
            aux2 = aux2 +" "+word

        meta_keywords = aux2
        #get the article tags
        tags = article.tags
        aux3 = ''

        for word in tags:
            aux3 = aux3 +" "+word

        tags = aux3
        to_return = [title, full_text, meta_description, summary, keywords, meta_keywords, tags]
        return list(map(self.clean_str, to_return))


    def save_pages(self, id, page_references):
        # title, text, main text, description
        for url in page_references:
            print(url)
            article = self.article_parse(url)
            KafkaProducer.send(
                'quickstart-events',
                {
                    'url': url,
                    'id': id,
                    'title': article[0],
                    'full_text': article[1],
                    'meta_description': article[2],
                    'summary': article[3],
                    'keywords': article[4],
                    'meta_keywords': article[5],
                    'tags': article[6]
                })

    def build_url(self, path):
        url_parse = urlparse(self._url)
        base_url = f'https://{url_parse.netloc}'

        return f'{base_url}{path}'

    def run(self, id, html):
        page_references = dict()

        soup_obj = BS(html, self.parser)
        page_references[self._url] = self._wikipedia_table_parser(soup_obj)

        self.save_pages(id, page_references)

        # This parser doesn't want to read more urls inside this website
        return set()
