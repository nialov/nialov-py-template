"""
Tasks for template development.
"""
from invoke import task


@task
def test(c, posargs=""):
    """
    Test template with scaffold Python project.
    """
    c.run(f"nox --session test -- {posargs}")
