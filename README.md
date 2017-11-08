# metaaldetectievondstmeldingen-dev

## deployment of dev environment for the 'metaaldetectievondstmeldingen' app

### build instructions

#### assumes
- access to OE private repos
- osx/linux environment
- docker installed
- python installed
- git
- your wildcards-private.ini files
- pycharm enterprise edition

#### general setup
```
# assumes you have access to OE private repos
git clone --recursive https://github.com/cecemel/metaaldetectievondstmeldingen-dev.git
cd metaaldetectievondstmeldingen-dev
# now, you have to add the development-private.ini and wildcards files on the right place, 
ask your colleagues for help if you don't know
```

#### building the frontend
```
TODO :-/
```

### building, migrating & init elastic, dummy data etc...
```
# assumes you are in folder metaaldetectievondstmeldingen-dev
docker-compose stop; docker-compose rm -f; #not required, but cleans your working environment
# assumes you are in metaaldetectievondstmeldingen-dev
python build_images.py [GITHUB_USER] [GITHUB_PASS];
python migrate_dbs.py;
python init_data.py;
```

#### reset backend one liner
```
docker-compose stop; docker-compose rm -f; rm -rf data/*; python build_images.py [GITHUB_USER] [GITHUB_PASS]; python migrate_dbs.py; python init_data.py;
```

### running in pycharm
see e.g. 
https://blog.jetbrains.com/pycharm/2017/03/docker-compose-getting-flask-up-and-running/

### rebuilding and running a dependent service
```
# e.g.
python build_images.py [GITHUB_USER] [GITHUB_PASS] storageprovider
```

### some git submodule tricks
- tutorial: https://git-scm.com/book/en/v2/Git-Tools-Submodules
- some good submodule SO: https://stackoverflow.com/questions/1030169/easy-way-to-pull-latest-of-all-git-submodules
- bringing *-dev repo up to data: git pull; git submodule update --init --recursive
- if new module is added: git submodule update --init 

### caveats-todos
- currently static map generator is broken -> docker won't find image.
- on slow networks, you'll might have to build a couple of times (2,3) again, because some scripts are not robust. needs fix
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
- if you want to test the flow tied to documentgenerator, you will have
    - to map metaaldetectievondstmeldingen-app to 127.0.0.1 in your /etc/hosts
    - build the frontend manually ( static/admin npm install; bower install)
    - add the template manually in the beheersinterface
    - This is TODO, if someone can help load a template programatically would be awesome
