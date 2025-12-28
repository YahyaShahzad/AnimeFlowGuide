import os, sys

# Ensure repo root is on PYTHONPATH for imports during CI
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def test_app_imports():
    from app import app
    assert app is not None


def test_app_config():
    from app import app
    with app.app_context():
        assert app.config is not None
