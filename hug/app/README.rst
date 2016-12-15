Hug sample app
--------------

A sample Hug app that demonstrates how you can do resource testing.
Functional and unit tests overlap on purpose to enable experiments with
unit testing.

Running the tests:
- install docker
- $ pip3 install --user tox # you have to have $HOME/.local/bin in $PATH
- $ tox

Running app (after running Tox for the first time): TODO
- run docker
- run REDIS_PORT=xxxx waitress-serve nananananana