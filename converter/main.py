import os
from pathlib import Path

import jinja2
import nbformat
from nbconvert import HTMLExporter

BASE_PATH = Path(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
OUTPUT_PATH = BASE_PATH/"converter/static/jupyter/nb"

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(BASE_PATH/"converter/templates")))
TEMPLATE = JINJA_ENV.get_template("html.html")

if __name__ == '__main__':
    files = (BASE_PATH/'notebooks').glob('**/*.ipynb')
    for file in files:
        file_path = str(file).split('/notebooks/')[-1]
        output_file_path = (OUTPUT_PATH/file_path).with_suffix('.html')
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file.absolute(), encoding="utf-8") as inputf, open(output_file_path.absolute(), 'w') as outputf:
            print(f'Converting {file.absolute()} to {output_file_path.absolute()}')
            nbdata = inputf.read()
            nb = nbformat.reads(nbdata, nbformat.current_nbformat)
            html_exporter = HTMLExporter(template_name='basic')
            (body, _) = html_exporter.from_notebook_node(nb)
            content = TEMPLATE.render(body=body)
            outputf.write(content)
