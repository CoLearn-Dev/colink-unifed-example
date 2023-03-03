# An example framework protocol in UniFed

This repo explains how to integrate a federated learning framework into UniFed as a [CoLink](https://colink.app/) protocol. You can follow the steps below to add new frameworks under UniFed.

## 1. Clone the repo

```bash
git clone https://<url-to-this-repo>
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

TBD

## Notes on trying out the code base

```bash
python test/test_all_config.py 
```
