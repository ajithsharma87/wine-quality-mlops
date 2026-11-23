import importlib.util


def test_mlproject_package_available():
    assert importlib.util.find_spec("Mlproject") is not None
