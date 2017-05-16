Txodds code test
================

A code challenge for Txodds recruitment.

Testing the code
----------------

The below instructions were checked on Ubuntu 16.04.

* Have Python 3.6.1 (at least) and Docker installed
* Install Tox: ``$ pip3 install --user tox``
* Run Tox: ``$ tox``

Running the code
----------------

* Do the steps from "Testing the code"
* ``$ . .tox/py36/bin/activate``
* ``$ docker run -d -p 6379:6379 redis:3.2.8-alpine``
* ``$ python -m txodds_code_test.url_extractor localhost 6379 &``
* ``$ python -m txodds_code_test.html_extractor localhost 6379 https://bultrowicz.com``
