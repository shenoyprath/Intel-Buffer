class TestApp:
    def test_has_all_blueprints(self, app):
        blueprints = "api",
        for blueprint in blueprints:
            assert blueprint in app.blueprints

    def test_has_all_extensions(self, app):
        extensions = "flask-jwt-extended",
        for extension in extensions:
            assert extension in app.extensions
