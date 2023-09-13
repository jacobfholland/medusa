import os

from dotenv import load_dotenv


def strip(input):
    return "/".join(input.split("/")[:-2])


def load_envs(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if ".env" in file:
                env_file_path = os.path.join(root, file)
                load_dotenv(env_file_path)


FILE_DIRECTORY = os.path.abspath(__file__)
PROJECT_DIR = strip(FILE_DIRECTORY)

load_envs(PROJECT_DIR)


class Config:
    APP_NAME = os.environ.get("APP_NAME")

    LOG_LEVEL = os.environ.get("LOG_LEVEL").upper()
    LOG_PATH = os.environ.get("LOG_PATH")
