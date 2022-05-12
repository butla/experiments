#!/bin/bash
set -e

root_dir=$(dirname $0)
root_dir=$(realpath ${root_dir})
venv_dir=${root_dir}/venv
v_python=${venv_dir}/bin/python

if [ ! -d ${venv_dir} ]; then
    python3.6 -m venv ${venv_dir}
    ${v_python} -m pip install -r ${root_dir}/requirements.txt
fi

(
cd ${root_dir}
${venv_dir}/bin/apistar run --no-debug --port 9090
)
