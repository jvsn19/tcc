from urllib import request, response, error
from .logger import Logger

class URLPages:
    '''
    This class converts the url string to a html
    '''

    @staticmethod
    def get_html(url: str):
        try:
            response = request.urlopen(url)
            return response
        except Exception as e:
            Logger.log_error(f'The URL {url} is invalid.\n{e}')
