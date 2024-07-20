#!/bin/bash

# Start Jenkins in the background
/sbin/tini -- /usr/local/bin/jenkins.sh &

# Wait for Jenkins to start
sleep 30  # Adjust the sleep duration as necessary

# Change ownership of Docker socket
chown root:docker /var/run/docker.sock
ls -l /var/run/docker.sock
id jenkins

# Wait for Jenkins to exit
wait
