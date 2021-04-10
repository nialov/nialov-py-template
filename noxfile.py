"""
Nox session tests for template.
"""
import nox
from pathlib import Path
from shutil import copytree


template_dir_name = "test_template"


@nox.session
def test(session: nox.Session):
    """
    Test template with nox session.
    """
    # Install dependencies
    session.install("poetry", "copier")

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

    # Run copier
    session.run("copier", "--force", "copy", str(current_dir), ".")

    # rm any existing poetry venv
    session.run("poetry", "env", "remove", "python", success_codes=[0, 1])

    # Install with poetry
    session.run("poetry", "install")

    # Update the local pyproject.toml file version
    session.run("poetry", "run", "invoke", "update-version")

    # Version should be updated by poetry-dynamic-versioning
    assert "0.0.0" not in Path("pyproject.toml").read_text()

    # Run tests that come from copier template files
    session.run("poetry", "run", "invoke", "make")
