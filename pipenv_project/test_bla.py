import env_var_config
import requests


def test_something():
    print(env_var_config.config)
    response = requests.get('http://www.wp.pl')
    assert response.status_code == 200
