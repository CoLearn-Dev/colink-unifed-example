# An example framework protocol in UniFed

This repo explains how to integrate a federated learning framework into UniFed as a [CoLink](https://colink.app/) protocol. You can follow the steps below to add new frameworks under UniFed.

## 1. Clone the repo

```bash
git clone git@github.com:CoLearn-Dev/colink-unifed-example.git
```

## 2. Update metadata

You should at least update the following 3 places:

- `setup.py`: Update the value of `FRAMEWORK_NAME`. All letters should be **lowercase**.
- Under `./src/unifed/frameworks/`: Rename the folder `example_framework` into `FRAMEWORK_NAME`.
- `colink.toml`:
  - Replace `unifed-example` with `unifed-<FRAMEWORK_NAME>`.
  - Replace all `colink-protocol-unifed-example` with `colink-protocol-unifed-<FRAMEWORK_NAME>`.
  - (Optional) Update the value of `description` to briefly describe your framework.

## 3. Install the package in an editable mode

Make sure you have Python 3.7+ installed. 
```bash
pip install -e .
```

## 4. Implement the protocol

- You should look into the file `./src/unifed/frameworks/<FRAMEWORK_NAME>/protocol.py`. It's recommended that you first look through the code and comments to get a general idea of how it works.
- `workload_sim.py` provides an expectation for how the external workload should look like. You can use it as a reference to compare with the framework that you are working with.
  - To try out the workload, in the root directory of the repo, run
```
unifed-example-workload client 1 ./log/1o.txt ./log/1l.txt
```
- You should also package the external workload and specify its instruction command in `colink.toml` under `install_script`.

## 5. Test the protocol

- The first step is to write a test configuration. You can look into `./test/configs/case_0.json` for an example. Note that for the case you construct, it should mainly serve the purpose of correctness testing (e.g. 1~2 epochs with a small model is usually sufficient). In this way, we can reproduce the correctness testing from a single host.
- Next, read `./test/test_all_config.py` to understand how to run the test.
  - To assert no error occurs when running certain configuration cases, in the root directory of the repo, run
```bash
pytest # note that you need to install pytest for this, via `pip install pytest`
```
  - To check the output for running certain cases, change the case string `target_case = "test/configs/case_0.json"` in `test_all_config.py` (note that this only works when you install with `-e` flag), then, in the root directory of the repo, run
```bash
python test/test_all_config.py 
```
- You can mark out the cases that are under development by adding `skip` in the name of the config (e.g. `skip_case_x.json`, so that pytest will skip those). You can still check the output of those cases by running `python test/test_all_config.py` directly.


## Recommended workflow for adding framework and hints

**Recommended workflow**
1. fork the repo
2. get familiar with the example
3. update the metadata
4. get familiar with and the external framework and package it
5. write one simple test case
6. write protocol to connect the interface
7. test the simple case, use `test_all_config.py` for testing during dev
8. iterate and add more test cases

**Hints**
- You don't have to follow the example exactly. You can change the structure of the code as long as you can make it work.
- For questions about CoLink, please ask them in #general channel in CoLink's Slack workspace ([link](https://join.slack.com/t/colearn-dev/shared_invite/zt-1gyr9fekz-sPgb_v0PA~XdROupQqy8bQ)).
- For questions about UniFed logging, you can refer to [this repo](https://github.com/AI-secure/FLBenchmark-toolkit/tree/main/tutorials/logging).
