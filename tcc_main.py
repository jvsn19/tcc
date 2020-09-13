CSV_PATH = '/Users/jvsn/Documents/tcc/csv_folder/links_webtables.csv'

from utils.readers import CSVReader
from utils.file_handler import FileHandler
from utils.crawlers import WikipediaCrawler
from utils.parsers import TCCParser

def main():
    urls = CSVReader.get_urls_from_csv(CSV_PATH)
    tcc_parser = TCCParser()
    wikipedia_crawler = WikipediaCrawler(tcc_parser)
    wikipedia_crawler.add_urls(urls)
    wikipedia_crawler.run()

if __name__ == '__main__':
    main()
