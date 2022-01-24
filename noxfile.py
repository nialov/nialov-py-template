"""
Nox session tests for template.
"""
from pathlib import Path
from shutil import copytree

import nox

TEMPLATE_DIR_NAME = "test_template"
CITATION_CFF = Path("CITATION.cff")

MAKE = "make"
PRE_COMMIT = "pre-commit"
CHANGELOG = "changelog"
TAG = "tag"
UPDATE_VERSION = "update-version"
UTF8 = "utf-8"
TEMPLATE_PYTHONS = ["3.8", "3.9"]


DISPATCH_STRS = [MAKE, PRE_COMMIT, CHANGELOG, TAG, UPDATE_VERSION]

nox.options.error_on_external_run = False


def initialize(session):
    """
    Initialize testing.
    """
    # Install dependencies
    session.install("copier", "pre-commit")

    # Save current dir to variable
    current_dir = Path(".").resolve()

    # Resolve test_template dir
    template_dir = current_dir / TEMPLATE_DIR_NAME

    # Create temporary directory
    tmp_dir = session.create_tmp()

    # Change to the temporary directory
    session.chdir(tmp_dir)

    # Copy test_template dir to temp dir
    copytree(template_dir, TEMPLATE_DIR_NAME)

    # Change to test_template dir in the cloned dir
    session.chdir(TEMPLATE_DIR_NAME)

    # Initialize git repo
    session.run("git", "init", external=True)

    # Run copier
    session.run("copier", "--force", "copy", str(current_dir), ".")

    # rm any existing poetry venv
    session.run(
        "poetry", "env", "remove", "python", success_codes=[0, 1], external=True
    )


def test_precommit(session):
    """
    Test pre-commit.
    """
    # Initialize pre-commit
    session.run("pre-commit", "install")
    session.run("pre-commit", "install", "--hook-type", "commit-msg")

    # Disable gpg sign
    session.run("git", "config", "commit.gpgsign", "false", external=True)

    # Stage and commit all
    # Will check commit hooks
    session.run("git", "add", ".", external=True)
    # Formatting hooks will change files resulting in unstaged files
    session.run(
        "git",
        "commit",
        "-m",
        "'feat: commit all files'",
        external=True,
        success_codes=[1],
    )
    # Stage and commit unstaged but with bad commit message
    session.run(
        "git",
        "commit",
        "-a",
        "-m",
        "wrong commit style!",
        external=True,
        success_codes=[1],
    )
    # Stage and commit unstaged with good commit message
    session.run(
        "git",
        "commit",
        "-a",
        "-m",
        "style: add formatted",
        external=True,
    )

    # Check all files with pre-commit
    session.run("pre-commit", "run", "--all-files")


def test_make(session):
    """
    Test doit all.
    """
    # Run tests that come from copier template files
    session.run("poetry", "run", "doit", "-n", "8", "-v", "0", external=True)


def test_update_version(session):
    """
    Test doit update-version.
    """
    # Update the local pyproject.toml file version
    session.run("poetry", "run", "doit", "update_version", external=True)

    # Version should be updated by poetry-dynamic-versioning
    assert "0.0.0\n" not in Path("pyproject.toml").read_text(UTF8)


def test_tag(session, tag: str):
    """
    Test doit tag.
    """
    # Update the all project strings with own script
    session.run("poetry", "run", "doit", "tag", f"--tag={tag}", external=True)

    # Version should be updated
    assert all(
        tag[1:] in Path(path).read_text(UTF8)
        for path in ("pyproject.toml", "CITATION.cff", "mypackage/__init__.py")
    )

    # Check that CITATION.cff exists and is not empty
    assert CITATION_CFF.exists() and len(CITATION_CFF.read_text(UTF8)) > 10


def test_changelog(session):
    """
    Test doit changelog.
    """
    # Generate changelog locally
    session.run("poetry", "run", "doit", "changelog", external=True)

    # Check that changelog exists and is non-empty
    changelog_path = Path("CHANGELOG.md")
    assert changelog_path.exists() and len(changelog_path.read_text(UTF8)) > 0


@nox.session(python=TEMPLATE_PYTHONS)
def test(session: nox.Session):
    """
    Test template with nox session.
    """
    if session.posargs is not None and len(session.posargs) > 0:
        dispatch_strs = session.posargs
        assert all(arg in DISPATCH_STRS for arg in dispatch_strs)
    else:
        dispatch_strs = DISPATCH_STRS

    initialize(session=session)

    if PRE_COMMIT in dispatch_strs:
        test_precommit(session=session)

    # Install with poetry
    session.run("poetry", "install", external=True)

    if MAKE in dispatch_strs:
        test_make(session=session)

    if UPDATE_VERSION in dispatch_strs:
        test_update_version(session=session)

    tag = "v0.0.5"
    if TAG in dispatch_strs:
        test_tag(session=session, tag=tag)
    if CHANGELOG in dispatch_strs:
        test_changelog(session=session)


@nox.session(python=TEMPLATE_PYTHONS[0])
def pre_commit(session: nox.Session):
    """
    Run pre-commit on all files.
    """
    session.run("pre-commit", "run", "--files", "noxfile.py", external=True)
