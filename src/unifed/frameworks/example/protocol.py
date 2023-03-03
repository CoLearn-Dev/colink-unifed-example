import os
import json
import sys
import subprocess
import tempfile
from typing import List

import colink as CL

from unifed.frameworks.example.util import store_error, store_return, GetTempFileName

pop = CL.ProtocolOperator(__name__)
UNIFED_TASK_DIR = "unifed:task"

def load_config_from_param_and_check(param: bytes):
    unifed_config = json.loads(param.decode())
    framework = unifed_config["framework"]
    assert framework == "example"
    deployment = unifed_config["deployment"]
    if deployment["mode"] != "colink":
        raise ValueError("Deployment mode must be colink")
    return unifed_config

def run_external_process_and_collect_result(cl: CL.CoLink, role: str):
    with GetTempFileName() as temp_log_filename, \
        GetTempFileName() as temp_output_filename:
        # start training procedure
        process = subprocess.Popen(
            [
                "unifed-example-workload",  
                # takes 3 args: mode(client/server), output, and logging destination
                role,
                temp_output_filename,
                temp_log_filename,
            ],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        # gather result
        stdout, stderr = process.communicate()
        returncode = process.returncode
        with open(temp_output_filename, "rb") as f:
            output = f.read()
        cl.create_entry(f"{UNIFED_TASK_DIR}:{cl.get_task_id()}:output", output)
        with open(temp_log_filename, "rb") as f:
            log = f.read()
        cl.create_entry(f"{UNIFED_TASK_DIR}:{cl.get_task_id()}:log", log)
        return json.dumps({
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "returncode": returncode,
        })


@pop.handle("unifed.example:server")
@store_error(UNIFED_TASK_DIR)
@store_return(UNIFED_TASK_DIR)
def run_server(cl: CL.CoLink, param: bytes, participants: List[CL.Participant]):
    unifed_config = load_config_from_param_and_check(param)
    return run_external_process_and_collect_result(cl, "server")


@pop.handle("unifed.example:client")
@store_error(UNIFED_TASK_DIR)
@store_return(UNIFED_TASK_DIR)
def run_client(cl: CL.CoLink, param: bytes, participants: List[CL.Participant]):
    unifed_config = load_config_from_param_and_check(param)
    return run_external_process_and_collect_result(cl, "client")
