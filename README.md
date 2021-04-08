# Documentation for nialov-py-template

This is a [copier](https://github.com/copier-org/copier) template for
Python 3.8 development.

Highly opionated and made for personal use.

## Short description of functionality

-   Testing framework based on `invoke` and `nox`.

-   Testing done with `pytest`, and code `coverage` is checked.

    -   `coverage-badge` is currently locally generated for use in `README.rst`.

-   Documentation with `sphinx`, theme `sphinx-rtd-theme`.

-   Contains GitHub Actions that call the aforementioned test frameworks
    (`lint` and `test-and-publish`).

    -   By default an
        [action](https://github.com/pypa/gh-action-pypi-publish) exists
        that will push to PyPI on tagged commits. However this requires
        a `PYPI_PASSWORD` API token to work.
    -   Non-tagged commits simply try building the package without
        pushing anywhere.

## Running tests

Run tests for the template with:

``` {.{bash}}
pipenv run invoke -c devtasks test
```

Testing uses another, scaffolded Python project at:
<https://github.com/nialov/nialov-py-template-test>
