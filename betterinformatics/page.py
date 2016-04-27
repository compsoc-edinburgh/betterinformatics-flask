from flask.views import View
from flask import render_template
from flask import Markup

import markdown


class Page(View):

    def __init__(self, page_name, md_path, pages):
        self.md_path = md_path
        self.page_name = page_name
        self.pages = pages
        self.load_content()

    def load_content(self):
        with open(self.md_path, 'r') as f:
            self.content = Markup(markdown.markdown(f.read()))

    def dispatch_request(self):
        # templates located in templates directory by default
        return render_template('page.html', content=self.content)
