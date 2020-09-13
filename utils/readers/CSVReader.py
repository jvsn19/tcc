from ..logger import Logger

class CSVReader:
    @staticmethod
    def get_urls_from_csv(csv_path, limit: int = -1):
        '''
        Function that reads a CSV file with urls. The CSV should follow the pattern:
        file.csv:
            <title> # This line will be ignored
            <url_1>
            ...
            <url_n>

        Arguments:
        path: URL to be donwloaded

        Optional arguments:
        limit: limit of the number of lines returned, default infinite

        Return:
        A set of URL. The set approach is to avoid repeated urls.
        '''
        output = set()

        try:
            with open(csv_path, 'r') as paths_file:
                paths_file.readline() # The first line is useless

                while limit:
                    line = paths_file.readline().strip()

                    if line == '':
                        break

                    output.add(line)
                    # If limit is negative, it value will never change
                    limit = limit - 1 if limit > 0 else limit

        except Exception as exception:
            Logger.log_error(f'Coudn\t parse the {csv_path} file. Error:\n{exception}')
        finally:
            return output
