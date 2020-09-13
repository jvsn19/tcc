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
        with open(csv_path, 'r') as paths_file:
            paths_file.readline() # The first line is useless
            output = set()

            while paths_file and limit:
                output.add(paths_file.readline())
                # If limit is negative, it value will never change
                limit = limit - 1 if limit > 0 else limit

            return output
