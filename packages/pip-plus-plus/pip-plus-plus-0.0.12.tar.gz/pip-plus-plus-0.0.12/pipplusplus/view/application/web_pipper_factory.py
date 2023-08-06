import json
import pathlib

from flask import render_template, url_for, request, make_response
from utils.url_msg_parser import UrlMessageListParser

from view.application.flask_piper import FlaskPipper


class WebPipperFactory(object):
    @classmethod
    def get_pipper(cls, **kwargs):
        pass


class FlaskPipperFactory(WebPipperFactory):
    LIST_CACHED_MSG = ""

    @classmethod
    def get_pipper(cls, **kwargs):
        app = FlaskPipper("Pipper")

        @app.route("/")
        def main_page():
            return render_template("home.html")

        @app.route("/about")
        def about():
            return render_template("about.html")

        @app.route("/submit", methods=['GET', 'POST'])
        def submit_request():
            data = json.loads(request.data)
            page, msg = app.run_command(data, req_type=request.method)
            if not msg:
                msg = "None"

            if page == "list":
                cls.LIST_CACHED_MSG = msg.decode("utf-8")
                msg = "None"

            resp_msg = {
                "page": page,
                "msg": msg
            }
            response = make_response()
            response.data = str(resp_msg).replace("'", "\"")
            return response

        @app.route("/success")
        @app.route("/success/<msg>")
        def success_page(msg=""):
            return render_template("success.html", msg=msg)

        @app.route("/failure")
        @app.route("/failure/<msg>")
        def failure(msg=""):
            return render_template("failure.html", msg=msg)

        @app.route("/list")
        @app.route("/list/<msg>")
        def list_packages(msg=""):
            msg = UrlMessageListParser.parse(cls.LIST_CACHED_MSG)
            return render_template("list.html", msg=msg)

        with app.test_request_context():
            cls.set_static()

        return app

    @classmethod
    def set_static(cls):
        proj_dir = pathlib.Path(__file__).parent.parent.parent
        static_path = proj_dir / "static"

        for static_file in static_path.iterdir():
            url_for("static", filename=static_file.name)
