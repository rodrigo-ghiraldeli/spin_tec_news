# Step 1 select default OS image
FROM alpine

# Step 2 Setting up environment
RUN apk add --no-cache python3-dev py3-pip && pip3 install --upgrade pip

# Step 3 Configure a software
# Defining working directory
WORKDIR /app

# Copying project files.
COPY . /app

# Installing dependencies.
RUN pip3 install -r requirements.txt

# Exposing an internal port
EXPOSE 5001

# Step 4 set default commands
# Default command
ENTRYPOINT [ "python3" ]

# These commands will be replaced if user provides any command by himself
CMD ["mongodb_flask.py"]