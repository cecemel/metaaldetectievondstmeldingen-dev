import os, shutil, time
import migrate_dbs

ELASTIC_INITS_FOLDER = "data-inits"
DOCKER_FILE = "Dockerfile-data-init"
DOCKER_REPO = "metaaldetectievondstmeldingen-dev"
ELASTIC_IMAGE = "geosolutions/elasticsearch-plugins"
ELASTIC_CONTAINER_NAME = "metaaldetectievondstmeldingen-elastic-init"
ELASTIC_DATA = "$(pwd)/data/elastic"
STORAGE_PROVIDER_IMAGE = "metaaldetectievondstmeldingen-dev/storageprovider:latest"
STORAGE_PROVIDER_CONTAINER_NAME = "storageprovider-init"
STORAGE_PROVIDER_DATA = "$(pwd)/data/storageprovider"
STORAGE_PROVIDER_DATA_MAP = "{}:/metaaldetectievondstmeldingen_store".format(STORAGE_PROVIDER_DATA)
REDIS_IMAGE = "redis"
REDIS_CONTAINER_NAME = "metaaldetectievondstmeldingen-redis-init"


def start_redis():
    try:
        stop_and_clean_redis_container()
    except:
        print("issue cleaning docker images, let's proceed and see...")

    _exec_command("docker run -p '6379:6379' --name {} {} &".format(REDIS_CONTAINER_NAME, REDIS_IMAGE))

    print("wait for redis to boot (10 secs)")
    time.sleep(10)
    _exec_command("docker run "
                  "--link {}:redis "
                  "metaaldetectievondstmeldingen-dev/redis-checker:latest"
                  .format(REDIS_CONTAINER_NAME))


def start_storage_provider():
    try:
        stop_and_clean_storage_provider_container()
    except:
        print("issue cleaning docker images, let's proceed and see...")

    _exec_command("mkdir -p {}".format(STORAGE_PROVIDER_DATA))
    _exec_command("docker run -p '6544:6544' --name {} -v {} {}&"
                  .format(STORAGE_PROVIDER_CONTAINER_NAME, STORAGE_PROVIDER_DATA_MAP, STORAGE_PROVIDER_IMAGE))

    print("wait for storage provider to boot (10 secs)")
    time.sleep(10)
    _exec_command("docker run "
                  "--link {}:storageprovider "
                  "metaaldetectievondstmeldingen-dev/storageprovider-checker:latest"
                  .format(STORAGE_PROVIDER_CONTAINER_NAME))


def start_elastic():
    # make sure it starts clean
    try:
        stop_and_clean_elastic_container()
    except:
        print("issue cleaning docker images, let's proceed and see...")

    _exec_command("docker run -p '9200:9200' --name {} -v {}:/usr/share/elasticsearch/data {} &".format(ELASTIC_CONTAINER_NAME,
                                                                                ELASTIC_DATA,
                                                                                ELASTIC_IMAGE))

    print("wait for elastic to boot (10 secs)")
    time.sleep(10)
    _exec_command("docker run "
                  "--link {}:elastic "
                  "metaaldetectievondstmeldingen-dev/elastic-checker:latest"
                  .format(ELASTIC_CONTAINER_NAME))


def run_elastic_init():
    try:
        start_storage_provider()
        start_elastic()
        start_redis()
        migrate_dbs.start_db()

        print('elastic ready, moving on...')

        current_path = os.path.dirname(os.path.realpath(__file__))
        migrations_dir = os.path.join(current_path, ELASTIC_INITS_FOLDER)

        assert os.path.isdir(migrations_dir), "Expected a data-inits dir..."

        migrations_folders = _listdir_not_hidden(migrations_dir)

        for folder in migrations_folders:
            target_folder = os.path.join(current_path, folder)

            docker_file = os.path.join(current_path, ELASTIC_INITS_FOLDER, folder, DOCKER_FILE)

            print("copy docker file ")
            shutil.copy(docker_file, target_folder)

            print("changing dir to {}".format(target_folder))
            os.chdir(target_folder)

            # do the docker build
            try:
                print("starting initialization")
                print("building image")
                docker_image_repo = "{}/{}-migration:latest".format(DOCKER_REPO, folder)
                _exec_command("docker build -f {} -t {} .".format(DOCKER_FILE, docker_image_repo))

                print("fire container and run migration")
                run_command = "docker run " \
                              "--link {}:elastic " \
                              "--link {}:postgres  " \
                              "--link {}:storageprovider " \
                              "--link {}:redis "\
                    .format(ELASTIC_CONTAINER_NAME,
                            migrate_dbs.DATABASE_CONTAINER_NAME,
                            STORAGE_PROVIDER_CONTAINER_NAME,
                            REDIS_CONTAINER_NAME)
                run_command += "{}".format(docker_image_repo)

                print("firing!")
                print(run_command)

                _exec_command(run_command)

            finally:
                # clean up
                print("changing dir back to {}".format(current_path))
                os.remove(os.path.join(target_folder, DOCKER_FILE))

                os.chdir(current_path)

    finally:
        stop_and_clean_redis_container()
        stop_and_clean_elastic_container()
        stop_and_clean_storage_provider_container()
        migrate_dbs.stop_and_clean_db_container()


def stop_and_clean_storage_provider_container():
    _exec_command("docker stop {}; docker rm {}".format(STORAGE_PROVIDER_CONTAINER_NAME,
                                                        STORAGE_PROVIDER_CONTAINER_NAME))


def stop_and_clean_elastic_container():
    _exec_command("docker stop {}; docker rm {}".format(ELASTIC_CONTAINER_NAME, ELASTIC_CONTAINER_NAME))


def stop_and_clean_redis_container():
    _exec_command("docker stop {}; docker rm {}".format(REDIS_CONTAINER_NAME, REDIS_CONTAINER_NAME))


def _exec_command(command):
    result = os.system(command)
    if not result == 0:
        raise Exception("Error while executing command {}".format(command))


def _listdir_not_hidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


if __name__ == '__main__':
    run_elastic_init()