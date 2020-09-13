from abc import ABC
from urllib import request, response, error, robotparser
from time import sleep

from ..logger import Logger

class BaseCrawler(ABC):
    '''
    Basic crawler implementation. A crawler is a bot that, given an url, downloads the html and,
    with a parser, get all the useful information from the webpage and continues to navigate throught
    the pages within the current one.
    The crawler works with a set of urls (set was choosen because it's a good/basic way to avoid repeated url)
    and a parser. Each url in this set will be downloaded and parsed by our parser. The parser decides what is
    the desired information. At the end of the parser phase, the parser should return new urls to add to our crawler,
    so it can move forward to new urls.
    params:
    - root_path: the root path from an url. For example: https://www.github.com
    - parser: the helper parser. The parser function is to, given an url, get all the useful information
      from it
    - useragent: the bot crawling the webpage.
      Default: *
    '''
    def __init__(self, root_path: str, parser, useragent = '*'):
        self.root_path = root_path
        self.useragent = useragent
        self.urls = set()
        self.sleep_time = 5
        self.parser = parser
        self._configure_robots_parser()

    # Properties
    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, new_parser):
        self._parser = new_parser

    # Private Methods
    def _configure_robots_parser(self):
        '''
        Configures the robots.txt. The robots.txt is responsible to avoid accessing forbidden pages
        '''
        self.robots_parser = robotparser.RobotFileParser(f'{self.root_path}/robots.txt')
        self.robots_parser.read()

    def _sleep(self):
        '''
        Method responsible for stopping the execution, to avoid overloading the website requests
        '''
        sleep(self.sleep_time)

    # public Methods
    def add_urls(self, urls):
        '''
        Method to add new urls to the crawler.
        '''
        self.urls.update(urls)

    def run(self):
        '''
        Method to start crawler.
        '''
        while self.urls:
            url = self.urls.pop()
            self._parser.root_url = url

            if not self.robots_parser.can_fetch(self.useragent, url):
                # robots.txt forbids us to parse this file
                continue

            try:
                response = request.urlopen(url)
                Logger.log_info(f'[{response.getcode()}] Request to {url} was successful.')
                new_urls = self.parser.run(response)

            except Exception as exception:
                raise exception

            # Add new urls to crawl
            self.add_urls(new_urls)

            if(len(self.urls) > 0):
                # If there is another url to get, wait 5 seconds
                self._sleep()

        Logger.log_info(f'Crawler finished.')
