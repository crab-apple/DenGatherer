import pytest


def pytest_addoption(parser):
    parser.addoption("--testcrawlers", action="store_true")


def pytest_runtest_setup(item):
    if 'crawler' in item.keywords and not item.config.getoption("--testcrawlers"):
        pytest.skip("Crawler tests not enabled")
