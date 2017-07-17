FROM python:3.5

RUN apt-get update
RUN apt-get install -y libgeos-c1 libgeos-3.4.2
RUN apt-get install -y imagemagick
RUN pip install sphinx
RUN apt-get install -y ghostscript
COPY requirements.txt /app/
COPY requirements-dev.txt /app/

WORKDIR "/app"

# TODO: fix this in a proper settings file
RUN pip install -e git+https://github.com/OnroerendErfgoed/pyramid_oeauth.git@1.2.0#egg=pyramid_oeauth
#RUN pip install --trusted-host 10.100.61.3 -i http://10.100.61.3/simple pyramid_oeauth==1.2.0
RUN pip install -e git+https://github.com/OnroerendErfgoed/pyoes.git@0.4.7#egg=pyoes
RUN pip install -e git+https://github.com/OnroerendErfgoed/oeauth.git@1.1.0#egg=oeauth
#RUN pip install --trusted-host 10.100.61.3 -i http://10.100.61.3/simple oeauth==1.1.0
RUN pip install -e git+https://github.com/OnroerendErfgoed/oe_geoutils.git@0.7.2#egg=oe_geoutils
RUN pip install -e git+https://github.com/OnroerendErfgoed/oe_utils.git@0.14.0#egg=oe_utils

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
COPY . /app

# build config files
WORKDIR "/app/deploy"
RUN python transform.py
WORKDIR "/app"

RUN python setup.py develop
CMD pserve development.ini