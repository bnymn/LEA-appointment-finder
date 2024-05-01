#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1280x2048x24 &

# Give Xvfb some time to start
sleep 1

# Start cron in the foreground
cron -f