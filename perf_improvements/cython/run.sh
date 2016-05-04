# need to be done in virtualenv with Cython
cythonize -i ../perf_test.py
mv ../perf_test.c ../perf_test.cpython-34m.so .
python perf_test_cython.py
