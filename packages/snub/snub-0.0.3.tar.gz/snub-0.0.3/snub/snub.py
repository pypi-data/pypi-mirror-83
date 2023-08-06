import os, re, json
from threading import Thread
from json2html import *
from .sync import Sync
from .dns import DNS


class Snub:

    __text_static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'text.static' + '.yml'))
    __static_list = []

    def make_search_regex(self, value):
        chars_to_escape = r"([.|/^&+%*=!<>?\\()-])"
        r = re.sub(chars_to_escape, r"\\\1", value)
        r = r"\b{}\b".format(r)
        return re.compile(r)

    def __check_text_list(self, value):
        snub_list = []
        count = 0
        search_rex = self.make_search_regex(value)
        self.snub_list = Sync().snub_list
        for snub in self.snub_list:
            if search_rex.search(self.snub_list[snub]):
                count += 1
                snub_list.append(snub)
        return snub_list

    def __check_dns_lists(self, value):
        return DNS().check(value)

    def __check_static_list(self, value):
        static_list = []
        if not self.__static_list:
            from .base import Base
            self.__static_list = Base().get_yml_data(self.__text_static_path)['static_list']
        for item in self.__static_list:
            if value == item:
                static_list.append(value)
        return static_list

    def check(self, value, text_list=False, dns_list=False, static_list=False):
        return_dict = {}
        if not text_list and not dns_list and not static_list:
            return_dict['text'] = self.__check_text_list(value)
            return_dict['dns'] = self.__check_dns_lists(value)
            return_dict['static'] = self.__check_static_list(value)
        elif text_list:
            return_dict['text'] = self.__check_text_list(value)
        elif dns_list:
            return_dict['dns'] = self.__check_dns_lists(value)
        elif static_list:
            return_dict['static'] = self.__check_static_list(value)
        return return_dict

    def analyze(self, value: str, text_list=False, dns_list=False, static_list=False, generate_report=False):
        from hopper import Hopper
        hopper = Hopper()
        header_analysis = hopper.analyse(value)
        if header_analysis:
            hop = 0
            for trail in header_analysis.get('trail'):
                trail['hop'] = hop
                hop += 1
                if trail.get('from'):
                    trail['snubbed_from'] = self.check(trail.get('from'), text_list=text_list, dns_list=dns_list, static_list=static_list)
                if trail.get('receivedBy'):
                    trail['snubbed_receivedBy'] = self.check(trail.get('receivedBy'), text_list=text_list, dns_list=dns_list, static_list=static_list)
        if generate_report:
            return self.__generate_report(header_analysis)
        return header_analysis

    def __generate_report(self, value):
        return json2html.convert(json=json.dumps(value))