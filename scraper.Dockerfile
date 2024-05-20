FROM python:3.11-slim

# Working directory in the container
WORKDIR /main_task

# Copy all files into the directory
COPY . /main_task

# Read requirements
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "scraper.py"]

# terminale:

# Patikrinti kokie container'iai runina
# docker container list
# docker image list

# Build an image:
# docker build .

# Run the docker:
# docker run (image id)

# docker run -d (image id)

# docker ps?

# docker kill (image id)

# Remove - docker image rm






