import os
from flask import Markup
import datetime

import markdown
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs, all_styles
import yaml


class Page(object):

    def __init__(self, name, md_path, history_path, history_file):
        self.md_path = md_path
        print(history_path)
        self.history_path = os.path.join(history_path,
                                         name + "/")
        self.history_file = history_file
        self.name = name
        self.init_data()

    def init_data(self):
        if not os.path.exists(self.history_path):
            os.mkdir(self.history_path)

        self.revision_num = 1
        self.revision_files = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                content = yaml.load(f)
                self.revision_num = content['revision_num']
                self.revision_files = content['revision_files']

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

        # get next file and write old content
        name = datetime.datetime.strftime(datetime.datetime.now(),
                                          '%Y%m%d%H%M%S%f')
        name = "r{0}-{1}.md".format(self.revision_num - 1, name)
        stamp_path = os.path.join(self.history_path, name)

        # create stamp file
        with open(stamp_path, "w+") as f:
            f.write(self.previous_md)
            print("Saved {}".format(stamp_path))
            self.revision_files.append(stamp_path)

        # update history file
        yaml_struct = {"revision_num": self.revision_num,
                       "revision_files": self.revision_files}
        yaml_dump = yaml.dump(yaml_struct)
        with open(self.history_file, "w") as f:
            f.write(yaml_dump)
            print("Updated {}".format(self.history_path))

    def update_md(self, md):
        self.previous_md = self.md
        self.previous_content = self.content  # use if needed to show diff
        self.revision_num += 1
        self.md = md
        self.content = self.read_md(self.md)

    def get_content(self):
        return self.content

    def get_md(self):
        return self.md

    def get_name(self):
        return self.name

    def get_revision(self):
        return self.revision_num
