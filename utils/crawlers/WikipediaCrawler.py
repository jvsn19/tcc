from .BaseCrawler import BaseCrawler

class WikipediaCrawler(BaseCrawler):
    def __init__(self, parser):
        super().__init__('https://en.wikipedia.org', parser)
