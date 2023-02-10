# Sustainability-Linked-Bonds
Thesis work repository

## Python Dependencies
Python dependencies are descibed in `Pipfile`:

**Python**
- `python`: 3.10

**Algorand SDKs**
- `py-algorand-sdk` >= 2.0.0
- `pyteal` >= 0.22.0
- `beaker-pyteal` >= 0.5.4

To set up the `venv` using `pipenv` enter:
```shell
pipenv install
```

## Algorand Sandbox
Install the Algorand `sandbox` and run it in `dev` mode:
```shell
./sandbox up dev
```

## Demo, Tests and CI
The _SBL dApp Demo_ can be executed as:
```shell
pipenv run python3 slb_app.py
```

The _SLB Test Suite_ is based on `pytest` (with `pytest-sugar` add-on). All tests
contained in `test` directory can be executed as:
```shell
pytest --verbose
```

The _SBL Continuous Integration_ pipeline is executed through GitHub Actions
structured in `slb_ci.yaml`.

## Linter and Code formatting
Code is formatted according the [Black](https://black.readthedocs.io/en/stable/) standard.

Code _linting_ is managed automatically by [pre-commit](https://pre-commit.com/)
```shell
pre-commit install
```

According `.pre-commit-config.yaml`:
```shell
pre-commit run --all-files
```

## Sustainability Linked Bond ABI
The ABI interface of SBL App is described in `/src/artifacts/application.json`.

## Sustainability Linked Bond TEAL
- Approval Program: `/src/artifacts/approval.teal`
- Clear Program: `/src/artifacts/clear.teal`
