from abc import ABC
from urllib import request, response, error, robotparser, parse
from time import sleep
from re import split
from utils.redis_client import RedisClient

from ..logger import Logger

class BaseCrawler(ABC):
    '''
    Basic crawler implementation. A crawler is a bot that, given an url, downloads the html and,
    with a parser, get all the useful information from the webpage and continues to navigate throught
    the pages within the current one.
    The crawler works with a set of urls and a parser. Each url in this set will be downloaded and parsed by our parser.
    The parser decides what isthe desired information. At the end of the parser phase, the parser should return new urls
    to add to our crawler, so it can move forward to new urls.
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
        self.redis = RedisClient()

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

    def _fix_url(self, url):
        '''
        Some URLs are codified in ASCII and urllib doesn't know how to deal with these urls.
        This method tries to fix the url using 'parse.quote'
        '''
        address = split(r'https?://', url)[~0]
        return f'https://{parse.quote(address)}'

    def _validate_url(self, url):
        '''
        Method to be implemented by the inherited classes. Is a validation where the user
        can avoid parsing an url
        '''
        return False

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
            id, url = self.urls.pop()
            self._parser.root_url = url

            if not self.redis.ping():
                Logger.log_error('Redis is not connected')
                return

            if not self.robots_parser.can_fetch(self.useragent, url) or self._validate_url(url) or (self.redis.get(url) is not None and redis.get(url) == 'OK'):
                # robots.txt forbids us to parse this file or this url should be ignored
                continue

            try:
                Logger.log_info(f'Start request to {url}.')
                response = request.urlopen(url)
                Logger.log_info(f'[{response.getcode()}] Request to {url} was successful.')
                new_urls = self.parser.run(id, response)

                # Add new urls to crawl
                self.add_urls(new_urls)
                self.redis.set(url, 'OK')

                if(len(self.urls) > 0):
                    # If there is another url to get, wait 5 seconds
                    self._sleep()

            except Exception as exception:
                Logger.log_error(f'Failed to get the {url}. Error:\n{exception}')
                self.redis.set(url, 'ERROR')
                fixed_url = self._fix_url(url)

                # Try again with new url
                if fixed_url != url:
                    Logger.log_info(f'Trying again {url} -> {fixed_url}')
                    self.add_urls(set(fixed_url))

        Logger.log_info(f'Crawler finished.')
