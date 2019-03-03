import os

from flask import current_app, send_file


def index(_path):
    """
    Redirect all paths/URLs to the home page. Vue will handle the routing from there.
    """

    dist_dir = current_app.config["DIST_DIR"]
    entry = os.path.join(dist_dir, "index.html")
    return send_file(entry)
