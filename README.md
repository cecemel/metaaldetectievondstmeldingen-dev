# metaaldetectievondstmeldingen-dev

## deployment of dev environment for the 'metaaldetectievondstmeldingen' app

### build instructions

#### assumes
- connected with vpn lm1
- osx/linux environment
- docker installed
- python installed
- git
- your wildcards-private.ini files
- pycharm enterprise edition

#### general setup
```
git clone --recursive ...
cd metaaldetectievondstmeldingen-dev
```

#### building the frontend
```
TODO :-/
```

### building, migrating & init elastic, dummy data etc...
```
# assumes you are in your virtual env
docker-compose stop; docker-compose rm -f; #not required, but cleans your working environment
# assumes you are in metaaldetectievondstmeldingen-dev
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
- if you get error HTTPError similar to: "401 Client Error: Unauthorized for url": restart your docker daemon
- scripts contain some hard coded parameters and should be cleaned
- currently, if you change code or config in dependent services, you will have to build and run every time again
- if you add a new dependent service and it needs a database, you will have to remove the postgres folder, and start the build from scratch
- working with private pypi server is still a hack, needs a fix
- a generic base image should be extract to speed up image build
- clean-up scripts, docker-compose should be sufficient for all migrations