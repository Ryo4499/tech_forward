import pytest
from run import create_app


@pytest.fixture(scope="session")
def app():
    return create_app("config.Testing")
