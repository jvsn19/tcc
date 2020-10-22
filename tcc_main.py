CSV_PATH = '/Users/jvsn/Documents/tcc/csv_folder/distinct_tables_allsignals.csv'

from utils.readers import CSVReader
from utils.crawlers import WikipediaCrawler
from utils.parsers import TCCParser
import pandas as pd

def main():
    df = pd.read_csv(CSV_PATH, nrows=3)[['table_id', 'table_url']].to_dict()
    id_url = [(df['table_id'][key], df['table_url'][key]) for key in df['table_id']]
    tcc_parser = TCCParser()
    wikipedia_crawler = WikipediaCrawler(tcc_parser)
    wikipedia_crawler.add_urls(id_url)
    wikipedia_crawler.run()

if __name__ == '__main__':
    main()
