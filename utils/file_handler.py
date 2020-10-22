import os

class FileHandler:
    class __FileHandler:
        def create_dir(self, path: str):
            os.makedirs(path, exist_ok=True)

        def write_tables_csv(self, name: str, path: str, content):
            if not os.path.exists(path):
                self.create_dir(path)

            with open(f'{path}/{name}.csv', 'a') as csv_file:
                csv_file.writelines(content + '\n')


    instance = None

    def _get_instance(self):
        if self.instance is None:
            self.instance = self.__FileHandler()

        return self.instance

    @classmethod
    def write_tables_csv(cls, name: str, path: str, content):
        instance = cls._get_instance(cls)
        return instance.write_tables_csv(name, path, content)
