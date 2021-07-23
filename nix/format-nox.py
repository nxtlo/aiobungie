import nox

@nox.session(reuse_venv=True)
def format_and_sort(session: nox.Session) -> None:
	session.install("-r", "dev-requirements.txt")
	session.run("isort", "aiobungie")
	session.run("black", "aiobungie")


@nox.session(reuse_venv=True)
def check_black(session: nox.Session) -> None:
	session.install("black")
	session.run("black", "aiobungie", "--check")