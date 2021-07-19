import nox

FILES = ['aiobungie/__init__.py', 'aiobungie/objects/__init__.py', 'aiobungie/utils/__init__.py']

def gen_stubs(session: nox.Session) -> None:
	session.install("-r", "requirements.txt", "-r", "dev-requirements.txt")
	session.run('stubgen', *FILES, '-o', '.', '--include-private', '--no-import')

@nox.session(reuse_venv=True)
def type_check(session: nox.Session) -> None:
	gen_stubs(session)
	session.install("-r", "requirements.txt", "-r", "dev-requirements.txt")
	session.run('mypy', 'aiobungie')

