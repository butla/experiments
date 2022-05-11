from itertools import chain

import docker
import port_for
import pytest
import redis

IMAGE = 'redis:3.2.8-alpine'


def download_image_if_missing(docker_client: docker.DockerClient):
    image_tags = chain(*[image.tags for image in docker_client.images.list()])
    if IMAGE not in image_tags:
        print(f"Docker image {IMAGE} doesn't exist, downloading...")
        docker_client.images.pull(IMAGE)


def start_redis_container(docker_client: docker.DockerClient):
    free_port = port_for.select_random()
    container = docker_client.containers.run(
        IMAGE,
        detach=True,
        ports={'6379/tcp': free_port})
    return container, free_port


@pytest.fixture(scope='session')
def redis_port_session():
    """Fixture that creates a Docker container with Redis for the whole test session and returns
    a port on localhost on which Redis will listen.
    """
    docker_client = docker.DockerClient(version='auto')
    download_image_if_missing(docker_client)
    container, redis_port_ = start_redis_container(docker_client)
    yield redis_port_
    container.remove(force=True)


@pytest.fixture(scope='function')
def redis_port(redis_port_session):
    yield redis_port_session
    redis_client = redis.Redis(port=redis_port_session)
    redis_client.flushall()
