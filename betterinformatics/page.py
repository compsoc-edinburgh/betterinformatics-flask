from flask import Markup

import markdown
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs, all_styles


class Page(object):

    def __init__(self, name, md_path):
        self.md_path = md_path
        self.name = name

    def load_content(self):
        with open(self.md_path, 'r') as f:
            self.md = f.read()
            self.content = self.read_md(self.md)

    def read_md(self, md):
        content = markdown.markdown(md)
        clean = bleach.clean(content,
                             markdown_tags, markdown_attrs, all_styles)
        return Markup(clean)

    def write_md(self):
        with open(self.md_path, 'w') as f:
            f.write(self.md)

    def update_md(self, md):
        self.md = md
        self.content = self.read_md(self.md)

    def get_content(self):
        return self.content

    def get_md(self):
        return self.md

    def get_name(self):
        return self.name
