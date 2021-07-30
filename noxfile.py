"""
Nox session tests for template.
"""
import nox
from pathlib import Path
from shutil import copytree


template_dir_name = "test_template"


@nox.session(python="3.8")
def test(session: nox.Session):
    """
    Test template with nox session.
    """
    # Install dependencies
    session.install("poetry", "copier", "pre-commit")

    # Save current dir to variable
    current_dir = Path(".").resolve()

    # Resolve test_template dir
    template_dir = current_dir / template_dir_name

    # Create temporary directory
    tmp_dir = session.create_tmp()

    # Change to the temporary directory
    session.chdir(tmp_dir)

    # Copy test_template dir to temp dir
    copytree(template_dir, template_dir_name)

    # Change to test_template dir in the cloned dir
    session.chdir(template_dir_name)

    # Initialize git repo
    session.run("git", "init", external=True)

    # Run copier
    session.run("copier", "--force", "copy", str(current_dir), ".")

    # rm any existing poetry venv
    session.run("poetry", "env", "remove", "python", success_codes=[0, 1])

    # Initialize pre-commit
    session.run("pre-commit", "install")
    session.run("pre-commit", "install", "--hook-type", "commit-msg")

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

    # Install with poetry
    session.run("poetry", "install")

    # Update the local pyproject.toml file version
    session.run("poetry", "run", "invoke", "update-version")

    # Version should be updated by poetry-dynamic-versioning
    assert "0.0.0\n" not in Path("pyproject.toml").read_text()

    # Test pre_commit task
    session.run("poetry", "run", "invoke", "pre-commit")

    # Run tests that come from copier template files
    session.run("poetry", "run", "invoke", "make")
