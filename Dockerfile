FROM python:3.10.5-slim

# Run as non-root user and make sure bash is the default shell
RUN useradd --create-home --shell /bin/bash app_user

# Change the working directory
WORKDIR /home/app_user

#RUN pip install
RUN pip install requests

# Change to previously-created user
USER app_user

# Copy application source code from Dockerfile directory in the host to /home/app_user
COPY . .

# Set bash as default command, invoked when docker runs
CMD ["bash"]