import yaml
import os.path

from flask import redirect, render_template, request, url_for
from flask import flash, make_response

from betterinformatics.page import Page


class BI(object):
    """Class generating views and page_names for BetterInformatics.

    Args:
        app (Flask): pointer to a Flask app.
        config_path (str): path to the configuration file.
        debug (Optional[bool]): Debugging flag used by Flask.app().
            Defaults to False.
    """

    def __init__(self, app, config_path=None):
        self.app = app
        self.page_names = []
        self.pages = {}

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
        self.debug = config["general"]["debug"]
        self.host = config["general"]["host"]

        self.history_file = config["history"]["file"]
        self.history_path = config["history"]["folder"]

        # pls make it
        assert(os.path.exists(self.history_path))

        print(config["pages"])
        self.page_names = config["pages"]
        self.index_page = config["general"]["index"]

        self.question = config["sign-in"]["question"]
        self.password = config["sign-in"]["password"]

    def gen_views(self):
        self.app.add_url_rule("/", 'index', self.index)

        print("# Generating page views!")
        for name in self.page_names:
            print("## Generating: " + name)
            path = os.path.join(self.pages_path, name + ".md")
            history_path = self.history_path
            history_file = os.path.join(self.history_path,
                                        self.history_file + name + ".yml")
            p = Page(name, path, history_path, history_file)
            p.load_content()
            self.pages[name] = p
            self.app.add_url_rule('/pages/<page>',
                                  methods=['get', 'post'],
                                  view_func=self.bi_page)
            self.app.add_url_rule('/pages/<page>/edit',
                                  methods=['get', 'post'],
                                  view_func=self.edit_page)
            self.app.add_url_rule('/pages/<page>/edit/publish',
                                  methods=['get', 'post'],
                                  view_func=self.publish_page)
        self.app.add_url_rule('/login', view_func=self.login)
        self.app.add_url_rule('/login/check', methods=['post'],
                              view_func=self.login_check)

    def bi_page(self, page):
        if not self.check_cookie():
            return redirect("/login")
        p = self.pages[page]
        name = p.get_name()
        content = p.get_content()

        return render_template("page.html", name=name, content=content,
                               pages=self.page_names)

    def edit_page(self, page):
        if not self.check_cookie():
            return redirect("/login")
        p = self.pages[page]
        name = p.get_name()
        revision = p.get_revision()
        content = p.get_md()
        logged = request.cookies.get("logged")

        if logged == "logged":
            return render_template("edit.html", name=name, content=content,
                                   pages=self.page_names, revision=revision)
        else:
            return redirect("/login")

    def publish_page(self, page):
        if not self.check_cookie():
            return redirect("/login")

        # get data
        text = request.form['textarea']
        p = self.pages[page]
        p.update_md(text)
        p.write_md()
        return redirect(url_for("bi_page", page=page))

    def login(self):
        return render_template("signin.html", name="Sign in",
                               question=self.question)

    def login_check(self):
        psswd = request.form["password"]
        if psswd == self.password:
            resp = make_response(redirect("/"))
            resp.set_cookie("logged", "logged")
            return resp
        else:
            flash("Wrong answer!")
            return redirect(url_for("login"))

    def index(self):
        if not self.check_cookie():
            return redirect("/login")
        return redirect("/pages/" + self.index_page)

    def run(self):
        """Runs the Flask application"""
        self.app.run(host=self.host, debug=self.debug)

    def check_cookie(self):
        value = request.cookies.get("logged")
        return value == "logged"
