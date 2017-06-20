# metaaldetectievondsten-dev

## deployment of dev environment for the 'metaaldetectievondsten' app

### build instructions

#### assumes
- connected with vpn lm1
- osx/linux environment
- docker installed
- python, python virtualenv, python virtualenvwrapper installed
- git
- postgres on your system
- your development-private.ini files
- npm and bower
- pycharm enterprise edition

#### general setup
```
git clone --recursive ...
cd metaaldetectievondsten-dev
mkvirtualenv metaaldetectievondsten-dev3.5 --python=python3.5
pip install -r requirements.txt
```

#### building the frontend
```
# assumes you are in metaaldetectievondsten-dev
cd metaaldetectievondsten/metaaldetectievondsten/static
npm install; bower install;
cd admin;
npm install; bower install;
```

### building, migrating & init elastic, dummy data etc...
```
# assumes you are in your virtual env
docker-compose stop; docker-compose rm -f; #not required, but cleans your working environment
# assumes you are in metaaldetectievondsten-dev
python build_images.py;
python migrate_dbs.py;
python init_data.py;
```

#### reset backend one liner
```
docker-compose stop; docker-compose rm -f; rm -rf data/*; python build_images.py; python migrate_dbs.py; python init_data.py;
```

### running in pycharm
see e.g. 
https://blog.jetbrains.com/pycharm/2017/03/docker-compose-getting-flask-up-and-running/

### rebuilding and running a dependent service
```
python build.py dossierdata
```

### caveats-todos
- if you modify the production.ini, you will have to build the image again
- docs need to be build automatically
- currently, only dummy data is imported, if you want data from the db.dump -> you will need to fiddle a little with the docker files...
- URI referencer is still not running locally
- if you get error HTTPError similar to: "401 Client Error: Unauthorized for url": restart your docker daemon
- scripts contain some hard coded parameters and should be cleaned
- currently, if you change code or config in dependent services, you will have to build and run every time again
- if you add a new dependent service and it needs a database, you will have to remove the postgres folder, and start the build from scratch
- working with private pypi server is still a hack, needs a fix
- a generic base image should be extract to speed up image build
- clean-up scripts, docker-compose should be sufficient for all migrations