#!/bin/bash
export COVERAGE_PROCESS_START=.coveragerc

coverage run -m py.test tests/
coverage combine
coverage report -m

