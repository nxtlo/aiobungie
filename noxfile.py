import nox

FILES = ['aiobungie/__init__.py', 'aiobungie/objects/__init__.py', 'aiobungie/utils/__init__.py']

def gen_stubs(session: nox.Session) -> None:
	session.install('.')
	session.run('stubgen', *FILES, '-o', '.', '--include-private', '--no-import')

@nox.session
def type_check(session) -> None:
	gen_stubs(session)
	session.install('.')
	session.run('mypy', 'aiobungie', external=True)