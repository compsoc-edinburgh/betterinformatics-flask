from flask import Flask


class BI(object):
    """Class generating views and pages for BetterInformatics.
    """

    def __init__(self, app, debug=False):
        """
        Args:
            app (Flask): pointer to a Flask app.
            debug (Optional[bool]): Debugging flag used by Flask.app().
                Defaults to False.
        """
        self.debug = debug
        self.app = app

    def run(self):
        self.app.run(debug=self.debug)
