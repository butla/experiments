import os
import sys
from urllib.parse import urljoin
import time
import uuid

import docker
import mountepy
import port_for
import pytest
import redis
import requests


REDIS_REPO = 'redis'
REDIS_IMAGE_TAG = '3.2.6-alpine'
REDIS_IMAGE = '{}:{}'.format(REDIS_REPO, REDIS_IMAGE_TAG)
DEFAULT_REDIS_PORT = 6379


def download_image_if_missing(docker_client):
    redis_images = docker_client.images(name=REDIS_REPO)
    proper_image_exists = bool([image for image in redis_images if REDIS_IMAGE in image['RepoTags']])
    if not proper_image_exists:
        print("Docker image {}:{} doesn't exist, trying to download... This may take a few minutes.")
        docker_client.pull(repository=REDIS_REPO, tag=REDIS_IMAGE_TAG)


def start_redis_container(docker_client):
    def wait_for_redis(port, timeout=5.0):
        start_time = time.perf_counter()
        redis_client = redis.Redis(port=port, db=0)
        while True:
            try:
                redis_client.ping()
                break
            except redis.connection.ConnectionError:
                time.sleep(0.01)
                if time.perf_counter() - start_time >= timeout:
                    raise TimeoutError('Waited too long for Redis to start accepting connections.')
    redis_port = port_for.select_random()
    host_config = docker_client.create_host_config(port_bindings={
        DEFAULT_REDIS_PORT: redis_port,
    })
    container_id = docker_client.create_container(REDIS_IMAGE, host_config=host_config)['Id']

    docker_client.start(container_id)
    wait_for_redis(redis_port)
    return container_id, redis_port


@pytest.yield_fixture(scope='session')
def redis_port():
    """
    Fixture that creates a Docker container with Redis for the whole test session.
    :return: Localhost's port on which Redis will listen.
    :rtype: int
    """
    docker_client = docker.Client(version='auto')
    download_image_if_missing(docker_client)
    container_id, redis_port = start_redis_container(docker_client)
    yield redis_port
    docker_client.remove_container(container_id, force=True)


@pytest.fixture(scope='session')
def redis_client_session(redis_port):
    return redis.Redis(port=redis_port, db=0)


@pytest.yield_fixture(scope='function')
def redis_client(redis_client_session):
    yield redis_client_session
    redis_client_session.flushdb()


@pytest.yield_fixture(scope='session')
def contact_app_session(redis_port):
    waitress_path = os.path.join(os.path.dirname(sys.executable), 'waitress-serve')
    app_command = [
        waitress_path,
        '--port', '{port}',
        '--host', 'localhost', # makes waitress run the external network offline
        '--call', 'contact_list.app:get_app']

    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    project_root_path = os.path.join(this_file_dir, '..')
    contact_service = mountepy.HttpService(
        app_command,
        env={'PYTHONPATH': project_root_path,
             'REDIS_PORT': str(redis_port)})

    contact_service.start()
    yield contact_service
    contact_service.stop()


@pytest.yield_fixture
def contact_app(contact_app_session, redis_client):
    return contact_app_session


def _dict_contains(dict_a, dict_b):
    """Checks if A contains B"""
    return dict_a.items() >= dict_b.items()


def test_store_and_get_contact(contact_app):
    contact = {
        'name': 'John Smith',
        'phone': {
            'mobile': '666-666-666',
            'work': '777-777-777',
        },
        'email': [
            'john@smith',
            'johnsmith@example.com',
        ]
    }

    post_resp = requests.post(urljoin(contact_app.url, '/contacts'), json=contact)

    assert post_resp.status_code == 201
    assert _dict_contains(post_resp.json(), contact)
    try:
        uuid.UUID(post_resp.json()['id'])
    except ValueError:
        pytest.fail('The returned contact ID was not a valid UUID.')

    get_resp = requests.get(urljoin(contact_app.url, post_resp.headers['location']))

    assert get_resp.json() == post_resp.json()
