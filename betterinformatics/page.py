from flask.views import View
from flask import render_template
from flask import Markup

import markdown


class Page(View):

    def __init__(self, md_path):
        self.md_path = md_path
        self.name = self.md_path
        self.load_content()

    def load_content(self):
        self.content = """
Chapter
=======

Section
-------

* Item 1
* Item 2
"""
        self.content = Markup(markdown.markdown(self.content))

    def dispatch_request(self):
        # templates located in templates directory by default
        return render_template('index.html', content=self.content)
