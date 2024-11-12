import tempfile
import os
from single import url_to_filename
from jinja2 import Environment, FileSystemLoader




class Nodo:
    def __init__(self, titolo: str, descrizione: str, link: str, img: str ):
        self.titolo = titolo
        self.descrizione = descrizione
        self.link = url_to_filename(link)
        self.img = img
        self.raiurl = link

def render_index( lista: list[Nodo], path: str ):
    env = Environment(loader = FileSystemLoader('tmpl'))
    template = env.get_template('pod.jinja')
    output = template.render(lista = lista)
    filename = os.path.join(path,"index.html")
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf8",
        delete=False,
        dir=os.path.dirname(filename),
        prefix=".tmp-single-",
        suffix=".html",
    )
    tmp.write(output)
    tmp.close()
    os.replace(tmp.name, filename)
