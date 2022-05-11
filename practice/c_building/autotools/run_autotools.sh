#!/bin/bash
set -v

autoscan

sed -e 's/FULL-PACKAGE-NAME/independent_app/' \
    -e 's/VERSION/0.0.1/' \
    -e 's|BUG-REPORT-ADDRESS|/dev/null|' \
    -e '10i\AM_INIT_AUTOMAKE' \
    < configure.scan > configure.ac

# required by autotools, we cheat by leaving them blank
touch NEWS README AUTHORS ChangeLog

autoreconf -iv
./configure
#make distcheck
make
