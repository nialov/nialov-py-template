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
    current_dir = Path(".").resolve()
    tmp_dir = session.create_tmp()
    session.chdir(tmp_dir)
    session.install("pipenv", "copier")
    session.run("git", "clone", scaffold_url, "--depth", "1", external=True)
    session.chdir(scaffold_dir)
    session.run("copier", "--force", "copy", str(current_dir), ".")
    session.run("pipenv", "--rm", success_codes=[0, 1])
    session.run("pipenv", "install", "--dev")
    session.run("pipenv", "run", "invoke", "make")
