#!/bin/bash
export COVERAGE_PROCESS_START=.coveragerc

coverage erase
coverage run -m py.test tests/
coverage combine
coverage report -m

