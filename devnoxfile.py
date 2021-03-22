"""
Nox session tests for template.
"""
import nox
from pathlib import Path

# template_url = "https://github.com/nialov/nialov-py-template"
scaffold_url = "https://github.com/nialov/nialov-py-template-test"

scaffold_dir = "nialov-py-template-test"


@nox.session
def test(session: nox.Session):
    """
    Test template with nox session.
    """
    # Save current dir to variable
    current_dir = Path(".").resolve()

    # Create temporary directory
    tmp_dir = session.create_tmp()

    # Change to the temporary directory
    session.chdir(tmp_dir)

    # Install dependencies
    session.install("pipenv", "copier", "versioneer")

    # git clone scaffold Python 3.8 project
    session.run("git", "clone", scaffold_url, "--depth", "1", external=True)

    # Change to the cloned dir
    session.chdir(scaffold_dir)

    # Run copier
    session.run("copier", "--force", "copy", str(current_dir), ".")

    # Rm any existing pipenv
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
