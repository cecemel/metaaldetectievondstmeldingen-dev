FROM onroerenderfgoed/docker-mapnik:b26cbb2018dc4b187bc86e710713ce83ef2f7546

RUN apt-get update
RUN apt-get install -y imagemagick

################################################################################
# Currently some oe depencies are still required to build this image.
# Provide --build-arg GITUSER=YOUR_USER --build-arg GITPW=YOUR_PW during build.
################################################################################

ARG GITUSER="USERNAME_NEEDED"
ARG GITPW="PASSWORD_NEEDED"
RUN pip install -e git+https://$GITUSER:$GITPW@github.com/OnroerendErfgoed/oeauth.git@1.1.0#egg=oeauth
RUN pip install -e git+https://$GITUSER:$GITPW@github.com/OnroerendErfgoed/pyramid_oeauth.git@1.2.0#egg=pyramid_oeauth


# static_map_generator deploy
RUN mkdir /app

COPY requirements-oe.txt /app/
COPY requirements.txt /app/
COPY requirements-dev.txt /app/

WORKDIR "/app"
RUN pip install -r requirements-oe.txt
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
COPY . /app

RUN python setup.py develop
CMD pserve development.ini