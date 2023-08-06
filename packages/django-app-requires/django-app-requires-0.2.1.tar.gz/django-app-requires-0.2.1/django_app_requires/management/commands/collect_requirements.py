import os

from fastutils import strutils

import djclick as click
from magic_import import import_from_string

from django.apps import apps
from django.conf import settings

def get_best_requirement(items):
    for item in items:
        print("# duplicate require: {0}".format(item))
    return items[-1]

@click.command()
@click.option("-a", "--all", is_flag=True)
def collect_requirements(all):
    requirements = []

    project_module_name = settings.WSGI_APPLICATION.split(".")[0]
    project_module = import_from_string(project_module_name)
    project_root = os.path.dirname(project_module.__file__)

    requirements_filenames = [
        os.path.join(project_root, "./requirements.txt"),
        os.path.join(project_root, "./extra_requirements.txt"),
    ]
    if all:
        for app in apps.get_app_configs():
            requirements_filenames.append(os.path.join(app.path, "./requirements.txt"))
            requirements_filenames.append(os.path.join(app.path, "./extra_requirements.txt"))
    else:
        root = os.path.abspath(os.path.dirname(os.sys.argv[0]))
        for app in apps.get_app_configs():
            app_path = os.path.abspath(app.path)
            if app_path.startswith(root):
                requirements_filenames.append(os.path.join(app.path, "./requirements.txt"))
                requirements_filenames.append(os.path.join(app.path, "./extra_requirements.txt"))

    for requirements_filename in requirements_filenames:
        if os.path.exists(requirements_filename):
            with open(requirements_filename, "r", encoding="utf-8") as fobj:
                requirements += [x.strip() for x in fobj.readlines() if x.strip()]
    requirements = list(set(requirements))
    requirements.sort()
    mapping = {}
    for requirement in requirements:
        if not requirement in mapping:
            mapping[requirement] = []
        mapping[requirement].append(requirement)
    requirements = []
    for requirement in list(mapping.keys()):
        requirement_items = mapping[requirement]
        if len(requirement_items) == 1:
            requirements.append(requirement_items[0])
        else:
            requirements.append(get_best_requirement(requirement_items))
    for requirement in requirements:
        print(requirement)
