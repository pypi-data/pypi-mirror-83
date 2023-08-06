import json
import subprocess
import sys
from pathlib import Path

import yaml


def wrap_cookiecutter():
    yaml_names = ('cookiecutter.yml', 'cookiecutter.yaml')
    for yaml_name in yaml_names:
        if Path(yaml_name).exists():
            yaml_to_json(yaml_name)
            break
    subprocess.run(['cookiecutter', *sys.argv[1:]])


def yaml_to_json(name: str):
    with open(name) as f:
        yaml_data = yaml.safe_load(f)
        json_data = json.dumps(yaml_data)

    with open('cookiecutter.json') as f:
        f.write(json_data)
