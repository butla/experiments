#!/bin/bash

nc localhost 8000 <<EOF
GET / HTTP/1.1

EOF
