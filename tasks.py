"""
Tasks for template development.
"""
from invoke import task


@task
def test(c):
    """
    Test template with scaffold Python project.
    """
    c.run("nox --session test")
