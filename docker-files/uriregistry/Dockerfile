FROM python:3.5

COPY requirements.txt /app/
COPY requirements-dev.txt /app/

WORKDIR "/app"
ARG GITUSER="USERNAME_NEEDED"
ARG GITPW="PASSWORD_NEEDED"
# TODO: fix this in a proper settings file
RUN pip install -e git+https://$GITUSER:$GITPW@github.com/OnroerendErfgoed/pyramid_urireferencer.git@0.6.0#egg=pyramid_urireferencer

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
COPY . /app

RUN python setup.py develop
CMD pserve development.ini