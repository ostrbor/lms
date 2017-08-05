from fabric.api import local, task
from fabric.context_managers import lcd

BASE_DIR = 'lms'


@task
def runserver():
    with lcd(BASE_DIR):
        local('./manage.py runserver')


@task
def migrate():
    with lcd(BASE_DIR):
        local('./manage.py makemigrations users')
        local('./manage.py makemigrations auction')
        local('./manage.py migrate')
        # local('./manage.py loaddata ../resources/fixtures/site.json')
        # local('./manage.py loaddata ../resources/fixtures/superuser.json')
        # local('./manage.py loaddata ../resources/fixtures/user.json')


@task
def shell():
    local(f'python {BASE_DIR}/manage.py shell_plus')


@task
def test():
    local(f'python {BASE_DIR}/manage.py test')
