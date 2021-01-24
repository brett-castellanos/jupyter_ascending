import argparse
from pathlib import Path

from jupyter_ascending._environment import PY_EXTENSION
from jupyter_ascending.handlers import jupyter_server
from jupyter_ascending.json_requests import SyncRequest
from jupyter_ascending.logger import J_LOGGER


@J_LOGGER.catch
def send(file_name: str):
    py_extension = f".{PY_EXTENSION}.py" if PY_EXTENSION else ".py"
    if py_extension not in file_name:
        return

    J_LOGGER.info(f"Syncing File: {file_name}...")
    file_name = str(Path(file_name).absolute())

    with open(file_name, "r") as reader:
        raw_result = reader.read()

    request_obj = SyncRequest(file_name=file_name, contents=raw_result)
    jupyter_server.request_notebook_command(request_obj)

    J_LOGGER.info("... Complete")


if __name__ == "__main__":
    J_LOGGER.disable("__main__")
    parser = argparse.ArgumentParser()

    parser.add_argument("--filename", help="Filename to send")

    arguments = parser.parse_args()
    send(arguments.filename)
