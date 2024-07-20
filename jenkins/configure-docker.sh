#!/bin/bash

# Change ownership of Docker socket
chown root:docker /var/run/docker.sock

# Ensure Jenkins user is part of the Docker group
usermod -aG docker jenkins

# Start Jenkins
exec /sbin/tini -- /usr/local/bin/jenkins.sh
