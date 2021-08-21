# Developing and Contributing to Aiobungie
First thing, thanks for taking the time to contribute. I appreciate that.

# Branches
Branches should look something like this.

* `patch/a-small-branch-info`
    * This should be for any type of PR thats not mentioned under.

* `meta/small-branch-info`
    * This should be for typos, markdown issues. typing issues. etc.

* `feature/a-small-feature-info`
    * This should be for feature implementation and requires more patches only.

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

## Pull requests

Before opening a PR, Please make sure that all nox tests passes.

Clone the repo and
install the normal and dev packages by running `pip install -r requirements.txt -r dev-requirements.txt`

__NOTE__: You should use a virtual enviroment here.

Make your changes.

run `nox` to make sure everything is working fine and all tests passed with no issues.

You can also run a specific session by running `nox -s mypy` or `nox -s mypy pdoc`

Commit your changes then push and open a PR.
