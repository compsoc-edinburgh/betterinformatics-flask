from flask.views import View
from flask import render_template
from flask import Markup

import markdown


class Page(object):

    def __init__(self, name, md_path):
        self.md_path = md_path
        self.name = name
        self.load_content()

    def read_content(self):
        with open(self.md_path, 'r') as f:
            self.content = Markup(markdown.markdown(f.read()))

    def write_content(self):
        with open(self.md_path, 'w') as f:
            f.write(self.content)

    def get_content(self):
        return self.content

    def get_name(self):
        return self.name
