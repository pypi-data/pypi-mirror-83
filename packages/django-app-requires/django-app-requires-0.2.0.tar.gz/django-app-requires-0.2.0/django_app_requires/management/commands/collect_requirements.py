import os

import djclick as click
from magic_import import import_from_string

from django.apps import apps
from django.conf import settings

@click.command()
def collect_requirements():
    requirements = []

    project_module_name = settings.WSGI_APPLICATION.split(".")[0]
    project_module = import_from_string(project_module_name)
    project_root = os.path.dirname(project_module.__file__)

    requirements_filenames = [
        os.path.join(project_root, "./requirements.txt"),
        os.path.join(project_root, "./extra_requirements.txt"),
    ]
    for app in apps.get_app_configs():
        requirements_filenames.append(os.path.join(app.path, "./requirements.txt"))
    
    for requirements_filename in requirements_filenames:
        if os.path.exists(requirements_filename):
            with open(requirements_filename, "r", encoding="utf-8") as fobj:
                requirements += [x.strip() for x in fobj.readlines() if x.strip()]
    requirements.sort()
    for requirement in requirements:
        print(requirement)
