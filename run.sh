#!/bin/bash

# Start the first process
source scraper_runner.sh

# Start the second process
python3 socket_server.py &
  
# Start the third process
python3 -m flask run --host=0.0.0.0 &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?