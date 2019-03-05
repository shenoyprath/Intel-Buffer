import os

from flask import current_app, send_file


# noinspection PyUnusedLocal
def index(path):
    """
    Redirect all non-API endpoints to the home page. Vue will handle the routing from there.
    """

    dist_dir = current_app.config["DIST_DIR"]
    entry = os.path.join(dist_dir, "index.html")
    return send_file(entry)
