#!/bin/bash
FIFO_FILE=my_fifo

# rm $FIFO_FILE
mkfifo $FIFO_FILE

echo "Just run something like this:"
echo 'for i in $(seq 100); do sleep 0.5; echo XXXXX > my_fifo; done'

echo "Listening for intput on ${FIFO_FILE} FIFO"
tail -f $FIFO_FILE
