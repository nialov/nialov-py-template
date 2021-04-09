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
    session.install("pipenv", "copier", "versioneer")

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

    # rm any existing pipenv
    session.run("pipenv", "--rm", success_codes=[0, 1])

    # Install with pipenv
    session.run("pipenv", "install", "--dev")

    # Update the local setup.py file
    session.run("pipenv", "run", "invoke", "requirements")

    # Run versioneer
    session.run("versioneer", "install")

    # Run tests that come from copier template files
    session.run("pipenv", "run", "invoke", "make")

    # Make sure versioneer files are not documented
    if Path("docs_src/mypackage._version.rst").exists():
        raise FileExistsError("Expected no apidoc on _version.py file.")
