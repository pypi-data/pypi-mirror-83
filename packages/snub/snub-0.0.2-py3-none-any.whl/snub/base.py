import yaml, json


class Base:

    def get_yml_data(self, path):
        with open(path, 'r') as ymlfile:
            return yaml.load(ymlfile, Loader=yaml.BaseLoader)
