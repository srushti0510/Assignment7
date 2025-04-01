# Use the official Python image from the Python Docker Hub repository as the base image
FROM python:3.12-slim-bullseye

# Set the working directory to /Assignment7 in the container
WORKDIR /Assignment7

# Create a non-root user named 'myuser' with a home directory
RUN useradd -m myuser

# Copy the requirements.txt file to the container to install Python dependencies
COPY requirements.txt ./

# Install only the necessary system dependencies for PIL/Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install the Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Before copying the application code, create the logs and qr_codes directories
# and ensure they are owned by the non-root user
RUN mkdir logs qr_codes && chown myuser:myuser logs qr_codes

# Copy the rest of the application's source code into the container, setting ownership to 'myuser'
COPY --chown=myuser:myuser . .

# Switch to the 'myuser' user to run the application
USER myuser

# Use the Python interpreter as the entrypoint and the script as the first argument
ENTRYPOINT ["python", "main.py"]

# Set the default argument (URL) for the script, but allow it to be overridden from the terminal
CMD ["--url", "https://github.com/srushti0510"]