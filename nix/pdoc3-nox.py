import nox

@nox.session(reuse_venv=True)
def pdoc(session: nox.Session) -> None:
	session.install("-r", "requirements.txt", "-r", "dev-requirements.txt", "pdoc3")
	session.run(
		"python",
		"-m",
		"pdoc",
		"aiobungie",
		"--html",
		"--output-dir",
		"docs",
		"--template-dir",
		"templates",
		"--force"
	)