import os, shutil, time

CWD = os.getcwd()
MIGRATIONS_FOLDER = "db-migrations"
ALEMBIC_FILE = "alembic-custom.ini"
DOCKER_FILE = "Dockerfile-migration"

DOCKER_REPO = "metaaldetectievondstmeldingen-dev"
DATABASE_IMAGE = "metaaldetectievondstmeldingen-dev/postgres:latest"
DATABASE_CONTAINER_NAME = "metaaldetectievondstmeldingen-migration-db"
DATABASE_DATA = "{}/data/postgres".format(CWD)
DATABASE_DUMP = "db.dump"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

def start_db():
    # make sure it starts clean
    try:
        stop_and_clean_db_container()
    except:
        print("issue cleaning docker images, let's proceed and see...")

    _exec_command("docker run -p 5432:5432 --name {} -v {}:/var/lib/postgresql/data {} &".format(DATABASE_CONTAINER_NAME,
                                                                        DATABASE_DATA,
                                                                        DATABASE_IMAGE))
    print("wait for migration db to boot (10 secs)")
    time.sleep(10)
    _exec_command("docker run --link {}:postgres metaaldetectievondstmeldingen-dev/postgres-checker:latest".format(DATABASE_CONTAINER_NAME))


def run_migrations():
    try:
        start_db()

        current_path = os.path.dirname(os.path.realpath(__file__))
        migrations_dir = os.path.join(current_path, MIGRATIONS_FOLDER)

        assert os.path.isdir(migrations_dir), "Expected a db-migrations dir..."

        migrations_folders =_listdir_not_hidden(migrations_dir)

        for folder in migrations_folders:
            target_folder = os.path.join(current_path, folder)

            alembic_file = os.path.join(current_path, MIGRATIONS_FOLDER, folder, ALEMBIC_FILE)

            print("copy file {} to {}".format(alembic_file, target_folder))
            shutil.copy(alembic_file, target_folder)

            docker_file = os.path.join(current_path, MIGRATIONS_FOLDER, folder, DOCKER_FILE)

            print("copy docker file ")
            shutil.copy(docker_file, target_folder)

            db_dump_file = os.path.join(current_path, MIGRATIONS_FOLDER, folder, DATABASE_DUMP)

            if os.path.isfile(db_dump_file):
                print("copy dump file")
                shutil.copy(db_dump_file, target_folder)

            print("changing dir to {}".format(target_folder))
            os.chdir(target_folder)

            # do the docker build
            try:
                print("starting migration")
                print("building image")
                docker_image_repo = "{}/{}-migration:latest".format(DOCKER_REPO, folder)
                _exec_command("docker build -f {} -t {} .".format(DOCKER_FILE, docker_image_repo))

                print("fire container and run migration")
                _exec_command("docker run --link {}:postgres {}".format(DATABASE_CONTAINER_NAME, docker_image_repo))
                print('done')

            finally:
                # clean up
                print("changing dir back to {}".format(current_path))
                os.remove(os.path.join(target_folder, ALEMBIC_FILE))
                os.remove(os.path.join(target_folder, DOCKER_FILE))

                db_dump_file = os.path.join(target_folder, DATABASE_DUMP)
                if os.path.isfile(db_dump_file):
                    os.remove(db_dump_file)
                os.chdir(current_path)

    finally:
        stop_and_clean_db_container()


def stop_and_clean_db_container():
    _exec_command("docker stop {}; docker rm {}".format(DATABASE_CONTAINER_NAME, DATABASE_CONTAINER_NAME))


# def _is_db_ready():
#     try:
#         conn = psycopg2.connect("host=localhost user={} password={}".format(POSTGRES_USER, POSTGRES_PASSWORD))
#         conn.close()
#         return True
#
#     except psycopg2.OperationalError as ex:
#         print("Connection failed: {0}".format(ex))
#         return False


def _exec_command(command):
    result = os.system(command)
    if not result == 0:
        raise Exception("Error while executing command {}".format(command))


def _listdir_not_hidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


if __name__ == '__main__':
    run_migrations()