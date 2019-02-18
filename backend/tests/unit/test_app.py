class TestApp:
    def test_has_all_blueprints(self, app):
        blueprints = "api",
        for blueprint in blueprints:
            assert blueprint in app.blueprints
