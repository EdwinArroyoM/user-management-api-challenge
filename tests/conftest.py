import pytest
import requests
from collections.abc import Iterator

BASE_URL = "http://localhost:3000"
AUTH_TOKEN = "mysecrettoken"
ENVIRONMENTS = ["dev", "prod"]


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def auth_token() -> str:
    return AUTH_TOKEN


@pytest.fixture(scope="session")
def environments() -> list[str]:
    return ENVIRONMENTS


@pytest.fixture()
def session() -> Iterator[requests.Session]:
    http_session = requests.Session()
    http_session.headers.update({"Content-Type": "application/json"})
    yield http_session
    http_session.close()

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        choices=["dev", "prod"],
        help="Run tests only for the selected environment.",
    )


def pytest_collection_modifyitems(config, items):
    selected_env = config.getoption("--env")

    if not selected_env:
        return

    kept_items = []
    deselected_items = []

    for item in items:
        callspec = getattr(item, "callspec", None)

        if callspec and "environment" in callspec.params:
            if callspec.params["environment"] == selected_env:
                kept_items.append(item)
            else:
                deselected_items.append(item)
        else:
            kept_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)
        items[:] = kept_items