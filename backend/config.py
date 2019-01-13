import os


class Config:
    ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "DevelopmentKey")

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, "frontend/dist")

    if not os.path.exists(DIST_DIR):
        raise NotADirectoryError(f"DIST_DIR not found: {DIST_DIR}")
