import glob
import json
import pytest


import colink as CL


def simulate_with_config(config_file_path):
    from unifed.frameworks.example.protocol import pop, UNIFED_TASK_DIR
    case_name = config_file_path.split("/")[-1].split(".")[0]
    with open(config_file_path, "r") as cf:
        config = json.load(cf)
    # use instant server for simulation
    ir = CL.InstantRegistry()
    config_participants = config["deployment"]["participants"]
    cls = []
    participants = []
    for p in config_participants:  # given user_ids are omitted and we generate new ones here
        role = p["role"]
        cl = CL.InstantServer().get_colink().switch_to_generated_user()
        pop.run_attach(cl)
        participants.append(CL.Participant(user_id=cl.get_user_id(), role=role))
        cls.append(cl)
    task_id = cls[0].run_task("unifed.example", json.dumps(config), participants, True)
    results = {}
    def G(key):
        r = cl.read_entry(f"{UNIFED_TASK_DIR}:{task_id}:{key}")
        if r is not None:
            if key == "log":
                return [json.loads(l) for l in r.decode().split("\n") if l != ""]
            return r.decode() if key != "return" else json.loads(r)
    for cl in cls:
        cl.wait_task(task_id)
        results[cl.get_user_id()] = {
            "output": G("output"),
            "log": G("log"),
            "return": G("return"),
            "error": G("error"),
        }
    return case_name, results


def test_load_config():
    # load all config files under the test folder
    config_file_paths = glob.glob("test/configs/*.json")
    assert len(config_file_paths) > 0


@pytest.mark.parametrize("config_file_path", glob.glob("test/configs/*.json"))
def test_with_config(config_file_path):
    if "skip" in config_file_path:
        pytest.skip("Skip this test case")
    results = simulate_with_config(config_file_path)
    assert all([r["error"] is None and r["return"]["returncode"] == 0 for r in results[1].values()])


if __name__ == "__main__":
    from pprint import pprint
    import time
    nw = time.time()
    target_case = "test/configs/case_0.json"
    print(json.dumps(simulate_with_config(target_case), indent=2))
    print("Time elapsed:", time.time() - nw)
