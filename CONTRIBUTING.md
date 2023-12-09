# Developing and Contributing to Aiobungie
First thing, thanks for taking the time to contribute. I appreciate that.

## Branches
Branches should look something like this.

* `task/a-small-branch-info`
    * This should be for any type of PR thats not mentioned under.

* `meta/small-branch-info`
    * This should be for typos, documentation, markdowns, minor issues.

* `feature/a-small-feature-info`
    * This should be for feature implementation and requires more tasks and reviews only.

* `bug/a-small-branch-info`
    * This should be for bug fixes only.


## Nox
nox is a helper to run all the tests for you. We currently have 8 tests.

* **format**: Formats and sorts the source files using `ruff` and `isort`.

* **lint**: `flake8` linting.

* **type_check**: Used for type checking the source files using `mypy`.

* **gen_stubs**: Used for generating stub files.

* **pdoc**: Docs generator.

* **pytest**: for testing and mocking aiobungie's `objects`.

* **spell**: Checks and fixes spelling mistakes in source files using `codespell`.

* **client**:
    Which are real HTTP tests for the base client, You need to configure something before you start.
    Check `Raw Client tests` section below.

You can list all available session by typing `nox -l`


## Coding style
- This project uses numpy style for the docs.
- Importing objects should be the module itself and not the absolute object. i.e.,

This is fine.
```py
import typing
from aiobungie.internal import enums

# non-runtime annotations.
if typing.TYPE_CHECKING:
    import collections.abc as collections

# Use the builtin tuple type and collections's sequence.
# We use the `|` pipe operator for union types.
Foo: tuple[str, ...] | str | None = None

# We annotate immutable sequence like objects with `collections.abc.Sequence[T]`
def get(components: collections.Sequence[Object]) -> str:
    components[0] = ... # Error.
    return ",".join(str(c) for c in components)

class Object:
    # Immutable sequences.
    name_list: collections.Sequence[str]

```
This doesn't follow the coding style.
```py
from typing import Union, Tuple, Optional
from aiobungie.internal.enums import MembershipType

Foo: Union[Tuple[Optional[str], ...], int] = 0
```

## [Type checking](https://www.python.org/dev/peps/pep-0484/)
This project is statically typed and uses `mypy` for the type checking, So everything must be type annotated.

## Raw Client tests
You may write tests for your new changes in `tests/aiobungie/test_client.py` under the specified class.

* Export your token as an env variable like this `export CLIENT_TOKEN='TOKEN'` for unix based systems.

If you're on windows, I recommend making a `.env` file in the root directory and write this `CLIENT_TOKEN='YOUR_TOKEN'`

`python-dotenv` will be used to parse the token from the `.env` file so you don't have to export it manually.
* Go to `tests/config.py` and set your account details there.
This is optional unless if you want to test your own data.


## Opening your first PR

- Clone the repo.
   - `git clone https://github.com/nxtlo/aiobungie/`

- You should use a virtual enviroment.
   - run inside the project `python -m venv .venv` to create the virtual env

- Install dev requirements.
   - `pip install -r dev-requirements`

- Checkout to a new branch and make your changes.
   - `git checkout -b task/refactor-method-x`

- Test all pipelines after finishing.
   - run `nox` to make sure everything is working fine and all tests passed with no issues.

   You can also run a specific session(s) by running `nox -s type_check` or `nox -s type_check pdoc`

Push and open a PR.
