FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnssutil3 \
    libnspr4 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxss1 \
    libxrandr2 \
    libatk1.0-0 \
    libgtk-3-0 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libxshmfence1 \
    wget \
    unzip \
    libatk-bridge2.0-0 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=114.0.5735.90 \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

# Install Chrome browser
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
