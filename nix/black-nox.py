import nox

@nox.session(reuse_venv=True)
def black(session: nox.Session) -> None:
	session.install("black")
	session.run("black", "aiobungie")


@nox.session(reuse_venv=True)
def check_black(session: nox.Session) -> None:
	session.install("black")
	session.run("black", "aiobungie", "--check")