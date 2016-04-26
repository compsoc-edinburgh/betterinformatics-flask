import yaml

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

        if not config_path:
            return

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
        print("# Generating views!")
        for page in self.pages:
            print("## Generating: " + page)
            self.app.add_url_rule("/" + page,
                                  view_func=Page.as_view(page, md_path=page))

    def run(self):
        """Runs the Flask application"""
        self.app.run(debug=self.debug)
