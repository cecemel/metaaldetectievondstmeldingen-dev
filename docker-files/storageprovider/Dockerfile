FROM python:2.7

RUN apt-get update

COPY . /app
WORKDIR "/app"

# parses the folder list and creates the parent folder. Careful not well tested!
RUN /bin/bash -c "cat development-private.ini | grep = |  cut -d '=' -f2 |  grep 'data$' | xargs  mkdir -p '{}'"
# removes the data from /path/data
RUN /bin/bash -c "cat development-private.ini | grep = |  cut -d '=' -f2 |  grep 'data$' | xargs  rm -rf '{}'"

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

RUN python setup.py install

# Serve
ENTRYPOINT pserve development.ini
