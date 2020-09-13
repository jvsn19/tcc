CSV_PATH = '/Users/jvsn/Documents/tcc/csv_folder/links_webtables.csv'

from utils.readers import CSVReader
from utils.parsers import WikipediaTableParser
from utils.file_handler import FileHandler

def main():
    urls = CSVReader.get_urls_from_csv(CSV_PATH, limit= 1)
    wikipedia_parser = WikipediaTableParser()
    wikipedia_parser.add_url(urls)
    file_references = wikipedia_parser.run()

    for url in file_references:
        file_name = url.split('/')[~0]
        FileHandler.write_tables_csv(file_name, './csvs', file_references[url])

if __name__ == '__main__':
    main()
