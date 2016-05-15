#!/bin/bash
export COVERAGE_PROCESS_START=.coveragerc

coverage erase
coverage erase # looks like a bug, but losing coverage isn't reported after one erase
coverage run -m py.test tests/
coverage combine
coverage report -m

