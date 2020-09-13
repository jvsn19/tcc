from abc import ABCMeta, abstractmethod

class BaseParser:
    __metaclass__ = ABCMeta

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
    def url(self, new_url):
        self._url = new_url

    @parser.setter
    def parser(self, new_parser):
        self._parser = new_parser

    @abstractmethod
    def run(self):
        '''
        [TODO]: Start method
        '''
        ...
