#!/bin/bash

python_code=$(cat <<EOF
import re, sys;
input_ = sys.stdin.read();
output_ = re.sub(r'(?:\d[a-z])', '[tu była cyfra i literka]', input_);
print(output_);
EOF
)

echo $python_code
echo asdfd123  f1 askdjfh4378fdg67 | python3 -c "$python_code"

# a better way
python3 <<EOF
import sys
print(sys.path)
EOF
