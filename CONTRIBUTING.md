# Developing and Contributing to Aiobungie
First thing, thanks for taking the time to contribute. I appreciate that.

# Branches
Branches should look something like this.

* `task/a-small-branch-info`
    * This should be for any type of PR thats not mentioned under.

* `meta/small-branch-info`
    * This should be for typos, markdown issues. typing issues. etc.

* `feature/a-small-feature-info`
    * This should be for feature implementation and requires more tasks and reviews only.

* `bug/a-small-branch-info`
    * This should be for bug fixes only.


# Nox
nox is a helper to run all the tests for you. We have 6 tests
* isort, black
    * file formatters.
* mypy, stubgen
    * mypy type checks and stubgen for generating stub files.
* pdoc3
    * docs generator.
* pytest
    * for testing and mocking aiobungie itself.
* codespell
    * File text spell checks.
* client_test and rest_test
    * Which are real tests for the base client and the rest client. 
    For this you'll need to export your token in an env variable like this `export CLIENT_TOKEN='TOKEN'` for unix based systems.

You can list all available session by typing `nox -l`

## Pull requests

Before opening a PR, Please make sure that all nox tests passes.

Clone the repo and
install the normal and dev packages by running `pip install -r requirements.txt -r dev-requirements.txt`

__NOTE__: You should use a virtual enviroment here.
run `python -m venv .venv` to create the virtual env

Make your changes.

run `nox` to make sure everything is working fine and all tests passed with no issues.

You can also run a specific session by running `nox -s mypy` or `nox -s mypy pdoc`

Commit your changes then push and open a PR.
