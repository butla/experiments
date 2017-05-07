Foreign principals scraper
==========================

Testing the code
----------------
Instructions were tested on Ubuntu 16.04.

- Move to directory containing this README.
- Be sure to have $HOME/.local/bin in $PATH
- Have Python 3.6 installed.
- Install Tox: ``$ pip install --user tox``
- Run Tox: ``$ tox``

Running the code
----------------

- Do the steps from "Testing the code".
- ``$ . .tox/py36/bin/activate``
- ``$ scrapy crawl foreign_principals -o foreign_principals.json``
