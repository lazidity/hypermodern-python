# noxfile.py
"""Nox sessions."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session

nox.options.sessions = "lint", "mypy", "safety", "tests"

locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.12"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.12"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=["3.12"])
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=["3.12"])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with=dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with=dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--requirement={requirements.name}", *args, **kwargs)


@nox.session(python=["3.12"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", "--install-types", "--non-interactive")
    session.run("mypy", *args)


package = "hypermodern_python"


@nox.session(python=["3.12"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--only=main", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)
