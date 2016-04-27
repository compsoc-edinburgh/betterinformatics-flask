import yaml
import os.path

from flask import redirect

from betterinformatics.page import Page

class BI(object):
    """Class generating views and pages for BetterInformatics.

    Args:
        app (Flask): pointer to a Flask app.
        config_path (str): path to the configuration file.
        debug (Optional[bool]): Debugging flag used by Flask.app().
            Defaults to False.
    """

    def __init__(self, app, config_path=None, debug=False):
        self.debug = debug
        self.app = app
        self.pages = []
        self.views = []

        self._load_config(config_path)

    def _load_config(self, config_path):
        """Loads configuration based on the given path."""
        # TODO: put defaults here.

        try:
            f = open(config_path, 'r')
            config = yaml.load(f)
            f.close()
        except Exception as exc:
            print(exc)
            return

        print(config)
        self.pages_path = config["general"]["pages_dir"]
        print(config["pages"])
        self.pages = config["pages"]

    def gen_views(self):
        self.app.add_url_rule("/", 'index', self.index)

        print("# Generating page views!")
        for page in self.pages:
            print("## Generating: " + page)
            path = os.path.join(self.pages_path, page + ".md")
            self.app.add_url_rule("/" + page,
                                  view_func=Page.as_view(page,
                                                         page_name=page,
                                                         md_path=path,
                                                         pages=self.pages))

    def index(self):
        return redirect("/home")

    def run(self):
        """Runs the Flask application"""
        self.app.run(debug=self.debug)
