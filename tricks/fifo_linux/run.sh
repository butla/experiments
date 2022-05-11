#!/bin/bash
python3 receiver.py &
python3 writer.py XXXXXXXXXXXXXXXXXXXXXXXXXXXXX &
python3 writer.py ----------------------------- &
python3 writer.py ///////////////////////////// &
