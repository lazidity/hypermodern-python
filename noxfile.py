# noxfile.py
import nox

@nox.session(python = [ "3.12" ])
def tests(session):
    args = session.posargs or [ "--cov", "-m", "not e2e" ]
    session.run("poetry", "install", external = True)
    session.run("pytest", *args)
