from os import makedirs, path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from single import RaiParser
from list_index import Nodo
from list_index import render_index

GENERI_URL = "https://www.raiplaysound.it/generi"


class RaiPlaySound:
    def __init__(self):
        self._seen_url = set()
        self._base_path = path.join(path.dirname(path.abspath(__file__)), "dist")
        makedirs(self._base_path, exist_ok=True)

    def parse_genere(self, url):
        result = requests.get(url)
        result.raise_for_status()
        soup = BeautifulSoup(result.content, "html.parser")
        elements = soup.find_all("article")
        for element in elements:
            url = urljoin(url, element.find("a")["href"])
            if url in self._seen_url:
                continue
            parser = RaiParser(url, self._base_path)
            try:
                parser.process()
                self._seen_url.add(url)
            except Exception as e:
                print(f"Error with {url}: {e}")

    def parse_generi(self) -> None:
        result = requests.get(GENERI_URL)
        result.raise_for_status()
        soup = BeautifulSoup(result.content, "html.parser")
        elements = soup.find_all("a", class_="block")
        generi = []
        for element in elements:
            url = urljoin(result.url, element["href"])
            generi.append(url)
        for genere in generi:
            self.parse_genere(genere)

    def parse_list(self) -> None:
        feeds = []
        list = [ 
                 "https://www.raiplaysound.it/programmi/zoomscattidalweb",
                 "https://www.raiplaysound.it/programmi/milanocrime",
                 "https://www.raiplaysound.it/programmi/revolution",
                 "https://www.raiplaysound.it/programmi/oltre-uninchiestasulluniversoincelitaliano",
                 "https://www.raiplaysound.it/playlist/tributattoo-lestoriedietroitatuaggi",
                 "https://www.raiplaysound.it/playlist/ilraccontodimezzanotte",
                 "https://www.raiplaysound.it/programmi/radio3mondo",
                 "https://www.raiplaysound.it/programmi/belve",
                 "https://www.raiplaysound.it/programmi/america7",
                 "https://www.raiplaysound.it/programmi/mappamondi",
                 "https://www.raiplaysound.it/programmi/checkpointcharlielacadutadelmuro",
                 "https://www.raiplaysound.it/programmi/insider-facciaafacciaconilcrimine",
                 "https://www.raiplaysound.it/programmi/primapagina",
                 "https://www.raiplaysound.it/playlist/fiabeeraccontichefannopaura",
                 "https://www.raiplaysound.it/playlist/josephconradnavigarenelprofondo",
                 "https://www.raiplaysound.it/programmi/bosscodiciesegreti"
        ]
        list.sort()
        for el in list:
            parser = RaiParser(el, self._base_path)
            try:
               out = parser.process(skip_programmi=False, date_ok=False)[0]
               feeds.append(Nodo(out.title, out.description, out.url, out._data['image']['url']))
            except Exception as e:
                print(f"Error with {el}: {e}")
        render_index(feeds,self._base_path)
              

def main():
    dumper = RaiPlaySound()
    dumper.parse_list()


if __name__ == "__main__":
    main()
