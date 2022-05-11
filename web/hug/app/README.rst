Hug sample app
--------------

A sample Hug app that demonstrates how you can do resource testing.
Functional and unit tests overlap on purpose to enable experiments with
unit testing.

Running the tests:
- install Docker
- create a virtualenv of Python 3.5 and activate it
- ``$ pip install -r requirements.txt -r tests/requirements.txt``
- ``$ py.test -v tests``

Running app:
- ``$ docker pull redis:3.2.6-alpine``
- ``$ docker run -d -p 6379:6379 redis:3.2.6-alpine``
- ``$ waitress-serve --host localhost --call contact_list.app:get_app``
