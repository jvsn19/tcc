from .BaseCrawler import BaseCrawler

class WikipediaCrawler(BaseCrawler):
    '''
    Implementation of a Wikipedia crawler. This crawler is developed to
    search in every website based on https://en.wikipedia.org.
    Implements the BaseCrawler class
    '''
    def __init__(self, parser):
        super().__init__('https://en.wikipedia.org', parser)
