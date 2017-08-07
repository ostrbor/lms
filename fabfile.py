from fabric.api import local
from fabric.api import task
from fabric.api import warn_only
from fabric.context_managers import lcd
import time

TIME_TO_WAIT = 5
DEVELOPMENT = 'docker-compose -f docker-compose/development.yml '
DJANGO_CMD = 'run --rm appserver python manage.py '
BASE_DIR = 'lms'


@task
def build_dev():
    local(DEVELOPMENT + 'build')


def init(docker_cmd):
    local(docker_cmd + DJANGO_CMD + 'makemigrations')
    time.sleep(TIME_TO_WAIT)
    local(docker_cmd + DJANGO_CMD + 'migrate')
    time.sleep(TIME_TO_WAIT)
    local(docker_cmd + DJANGO_CMD + 'createsuperuser')


@task
def init_dev():
    init(DEVELOPMENT)


@task
def up_dev():
    local(DEVELOPMENT + 'up')


@task
def run():
    with lcd(BASE_DIR):
        local('./manage.py runserver')


@task
def migrate():
    with lcd(BASE_DIR):
        local('./manage.py makemigrations auction')
        local('./manage.py migrate')
        local('./manage.py loaddata ../resources/fixtures/user.json')
        local('./manage.py loaddata ../resources/fixtures/auction.json')


@task
def shell():
    local(DEVELOPMENT + DJANGO_CMD + 'shell_plus')


@task
def down():
    with warn_only():
        local(DEVELOPMENT + 'down --remove-orphans')


@task
def test():
    local(DEVELOPMENT + DJANGO_CMD + 'test')
