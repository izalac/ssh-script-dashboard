FROM python:3.13.2-alpine3.21

# System update
RUN apk update
RUN apk upgrade
RUN apk add build-base
RUN python3 -m pip install --upgrade pip

# Install requirements
WORKDIR /ssh-script-dashboard
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#adds the rest of the files
COPY . .

# Add custom CA certificate - if you need one, add it in as config/cacert.crt and uncomment:
# RUN apk --no-cache add ca-certificates
# COPY config/cacert.crt /usr/local/share/ca-certificates
# RUN update-ca-certificates
# ENV REQUESTS_CA_BUNDLE /python-docker/config/cacert.crt

# Unit tests are on - image build fails if they fail
RUN python3 -m unittest

# Networking
EXPOSE 5000

# Runs the container
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
