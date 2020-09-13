from abc import ABC
from urllib import request, response, error, robotparser
from time import sleep

from ..logger import Logger

class BaseCrawler(ABC):
    def __init__(self, root_path: str, parser):
        self.root_path = root_path
        self.useragent = '*'
        self.urls = set()
        self.sleep_time = 5
        self._parser = parser
        self._configure_robots_parser()

    # Properties
    @property
    def parser(self):
        if self._parser is None:
            Logger.log_error("Parser not defined")
            return None
        return self._parser

    @parser.setter
    def parser(self, new_parser):
        self._parser = new_parser

    # Private Methods
    def _configure_robots_parser(self):
        self.robots_parser = robotparser.RobotFileParser(f'{self.root_path}/robots.txt')
        self.robots_parser.read()

    def _sleep(self):
        sleep(self.sleep_time)

    # public Methods
    def add_urls(self, urls):
        self.urls.update(urls)

    def run(self):
        while self.urls:
            url = self.urls.pop()
            self._parser.root_url = url
            if not self.robots_parser.can_fetch(self.useragent, url):
                continue

            try:
                response = request.urlopen(url, timeout=2)
                Logger.log_info(f'[{response.getcode()}] Request to {url} was successful.')
                new_urls = self.parser.run(response)

            except Exception as exception:
                raise exception

            self.add_urls(new_urls)

            if(len(self.urls) > 0):
                # If there is another url to get, wait 5 seconds
                self._sleep()

        Logger.log_info(f'Crawler finished.')
        return 0
