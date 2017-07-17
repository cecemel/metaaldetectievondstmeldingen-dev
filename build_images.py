import os, shutil, subprocess, sys

POSTGRES_FOLDER = "postgres"
DEVELOPMENT_PRIVATE_FILES_FOLDER = "docker-files"
DOCKER_REPO = "metaaldetectievondstmeldingen-dev"
DOCKER_FILE = "Dockerfile"


def build_db():
    current_path = os.path.dirname(os.path.realpath(__file__))
    db_dir = os.path.join(current_path, POSTGRES_FOLDER)

    print("start of docker build")
    print("changing dir to {}".format(db_dir))
    os.chdir(db_dir)

    try:
        repo_image = "{}/{}:latest".format(DOCKER_REPO, POSTGRES_FOLDER)
        command = "docker build -t {} .".format(repo_image)
        _exec_command(command)

    finally:
        os.chdir(current_path)


def build_docker_modules(git_user, git_pw, modules=[]):
    current_path = os.path.dirname(os.path.realpath(__file__))
    docker_files_dir = os.path.join(current_path, DEVELOPMENT_PRIVATE_FILES_FOLDER)

    assert os.path.isdir(docker_files_dir), "Expected a docker-files dir..."

    if not modules:
        docker_files_folders = _listdir_not_hidden(docker_files_dir)
    else:
        docker_files_folders = modules

    for folder in docker_files_folders:
        try:

            target_folder = os.path.join(current_path, folder)

            docker_file = os.path.join(docker_files_dir, folder, DOCKER_FILE)

            print("start of docker build")
            shutil.copy(docker_file, target_folder)
            print("changing dir to {}".format(target_folder))
            os.chdir(target_folder)

            repo_image = "{}/{}:latest".format(DOCKER_REPO, folder)
            command = "docker build --build-arg GITUSER={} --build-arg GITPW={} -t {} .".format(git_user, git_pw, repo_image)
            _exec_command(command)

        finally:
            print("changing dir back to {}".format(current_path))
            os.remove(os.path.join(target_folder, DOCKER_FILE))
            os.chdir(current_path)


def _exec_command(command):
    result = os.system(command)
    if not result == 0:
        raise Exception("Error while executing command {}".format(command))


def _listdir_not_hidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


if __name__ == '__main__':
    if len(sys.argv[1:]) < 2:
        print("please provide username and password for OE github")
        exit(1)

    build_db()
    git_user_name = sys.argv[1]
    git_pw = sys.argv[2]

    images = []
    if len(sys.argv[1:]) > 2:
        images = sys.argv[3:]

    build_docker_modules(git_user_name, git_pw, modules=images)