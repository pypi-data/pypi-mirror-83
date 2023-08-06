import json, os, requests, time, datetime
from threading import Thread
from .base import Base


class Sync(Base):

    __SYNCED_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'snub_list' + '.json'))
    __text_blackhole_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'text.blackhole' + '.yml'))
    __blackhole_list = []

    def __init__(self, force=False):
        if not self.__blackhole_list:
            self.__blackhole_list = self.get_yml_data(self.__text_blackhole_path)['blackhole']
        self.__snub_list = {}
        self._threads = []
        if not self.snub_list:
            self.download()
        elif self.updated >= (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat():
                self.download()
        if force:
            self.download()

    @property
    def updated(self):
        with open(self.__SYNCED_DATA_PATH) as json_file:
            last_updated = json.load(json_file)['updated']
            return last_updated

    @updated.setter
    def updated(self, value):
        with open(self.__SYNCED_DATA_PATH, "w") as f:
            json.dump(value, f)

    @property 
    def snub_list(self):
        try:    
            with open(self.__SYNCED_DATA_PATH, 'r') as f:
                return json.loads(f.read())
        except:
            return False

    @snub_list.setter
    def snub_list(self, value):
        self.download()

    def _download_list(self, url):
        try:
            with requests.Session() as s:
                download = s.get(url)
                decoded_content = download.content.decode('utf-8', errors='ignore')
                self.__snub_list[url] = decoded_content
        except:
            pass

    def _download_lists(self):
        for url in self.__blackhole_list:
            t = Thread(target=self._download_list, args=(url,))
            t.start()
            time.sleep(0.1)
            self._threads.append(t)

    def download(self):
        self.__snub_list['updated'] = datetime.datetime.now().isoformat()
        self._download_lists()
        while len(self._threads) > 0:
            new_threads = []
            for t in self._threads:
                if t and t.isAlive():
                    new_threads.append(t)
            self._threads = new_threads
            time.sleep(1)
        self.updated = self.__snub_list
