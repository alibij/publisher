import json
import re
import subprocess
import os

from common.exceptions import NotAcceptableError
from config import env_config


async def get_all_configs(directory: str):

    all_files = os.listdir(directory)
    conf_files = []
    data = {}

    for f in all_files:
        if f.endswith('.conf') and f != "example.conf":
            conf_files.append(f)

    try:
        for file in conf_files:
            with open(f'{directory}/{file}', 'r') as f:
                d = json.load(f)
                if d.keys() & data.keys():
                    raise NotAcceptableError(
                        f"Duplicate data find in {file}")
                data.update(d)
    except Exception as e:
        raise NotAcceptableError(f"CONFIG FILE ERROR : {e}")
    return data


def create_command(command: str):
    command = re.sub(r'\s+', ' ', command).strip()
    return command


def run_command(command: str, work_dir: str = "."):
    try:
        res = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=work_dir  # Set the working directory
        )
        return res.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
