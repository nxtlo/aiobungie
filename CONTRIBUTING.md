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
* pdoc
    * docs generator.
* pytest
    * for testing and mocking aiobungie itself.
* codespell
    * File text spell checks.
* client_test and rest_test
    - Which are real tests for the base client and the rest client. 
    For this you'll need to export your token in an env variable like this `export CLIENT_TOKEN='TOKEN'` for unix based systems.

    If you're on windows i recommend making a `.env` file in the root directory and write this `CLIENT_TOKEN='TOKEN'`

You can list all available session by typing `nox -l`

## Notes

### Coding style
- This project uses numpy style for the docs.
- Importing stuff should be the module itself and not the absolute object. i.e.,

This is fine.
```py
import typing
from aiobungie.internal import enums

# non-runtime annotations.
if typing.TYPE_CHECKING:
    import collections.abc as collections

# Use the builtin tuple type and collections's Collection.
foo = typing.Union[tuple[str, ...], collections.Collection[str]]
```
This doesn't follow the coding style.
```py
from typing import Union, Tuple, Collection
from aiobungie.internal.enums import MembershipType

foo = Union[Tuple[str, ...], Collection[str]]

```

### [Type checking](https://www.python.org/dev/peps/pep-0484/)
This project is statically typed and uses mypy for the type checking, So everything should be type annotated.

### Client and RESTClient tests
You may write tests for your new changes(if so) at `tests/_raw`.

## Opening your first PR

- Clone the repo.
   - `git clone https://github.com/nxtlo/aiobungie/`

- You should use a virtual enviroment.
   - run inside the project `python -m venv .venv` to create the virtual env

- Install dev requirements.
   - `pip install -r dev-requirements`

- Checkout to a new branch and make your changes.
   - `git checkout -b task/small-info-about-the-task`

- Test all pipelines after finishing.
   - run `nox` to make sure everything is working fine and all tests passed with no issues.

   You can also run a specific session by running `nox -s type_check` or `nox -s type_check pdoc`

Push and open a PR.
