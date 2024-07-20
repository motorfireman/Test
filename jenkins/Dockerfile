FROM jenkins/jenkins:lts

USER root

# Install Python, Docker CLI, and Git
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv docker.io git && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Copy the configuration script
COPY configure-docker.sh /usr/local/bin/configure-docker.sh

# Make the script executable
RUN chmod +x /usr/local/bin/configure-docker.sh

# Configure Git
ARG GIT_USER_NAME
ARG GIT_USER_EMAIL

RUN git config --global user.name "${GIT_USER_NAME}" && \
    git config --global user.email "${GIT_USER_EMAIL}"

# Switch back to the Jenkins user
USER jenkins

# Run the configuration script when the container starts
ENTRYPOINT ["/usr/local/bin/configure-docker.sh"]
