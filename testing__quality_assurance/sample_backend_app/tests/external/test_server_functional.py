import pytest
from redis import Redis
import requests
import tenacity


@pytest.fixture(scope="session")
def docker_services(docker_services):
    """Waits until the app in Docker becomes responsive.
    Overwrites the fixture from pytest-docker.
    """
    waiter_port = docker_services.port_for("waiter", 8080)
    waiter_url = f"http://localhost:{waiter_port}"
    _wait_for_compose(waiter_url)
    return docker_services


@tenacity.retry(
    stop=tenacity.stop_after_delay(10),
    wait=tenacity.wait_fixed(0.1),
)
def _wait_for_compose(app_url: str):
    response = requests.get(app_url)
    response.raise_for_status()


@pytest.fixture(scope="session")
def app_url(docker_services):
    app_port = docker_services.port_for("api", 8080)
    return f"http://localhost:{app_port}"


def test_names_from_greetings_get_saved(app_url, docker_services):
    names = ["Wieńczysław", "Spycigniew", "Perystaltyka"]
    for name in names:
        requests.get(f"{app_url}/hello/{name}")

    redis_port = docker_services.port_for("database", 6379)
    redis = Redis(port=redis_port)
    saved_names = redis.lrange("names", 0, -1)
    assert {name.decode() for name in saved_names} == set(names)
