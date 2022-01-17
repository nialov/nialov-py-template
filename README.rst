Documentation for nialov-py-template
====================================

This is a `copier <https://github.com/copier-org/copier>`__ template for
Python ``3.8`` development.

Highly opinionated and made for personal use.

Short description of functionality
----------------------------------

-  Testing framework based on `doit <https://github.com/pydoit/doit>`__
   and `nox <https://github.com/theacodes/nox>`__.

   -  Allows replication of continous integration (=ci) tests locally.

   -  Continuous integration is conducted with ``GitHub Actions``.

   -  In ci, ``doit`` tasks ``ci-test``, ``format-and-lint``, ``docs``,
      ``citation`` and ``build`` are called.

      -  Note that ``docs`` are hosted on ``ReadTheDocs``, the task is only ran
         to test the building with task that mimigs ``ReadTheDocs``.

      -  An
         `action <https://github.com/pypa/gh-action-pypi-publish>`__ exists
         that will push to PyPI on tagged commits.

         -  However this requires a ``PYPI_PASSWORD`` API token to work.

         -  See ``build-and-publish`` job in workflow file.

      -  Non-tagged commits simply try building the package without pushing
         anywhere.

-  Testing of code is done with `pytest
   <https://github.com/pytest-dev/pytest>`__.

   -  Code `coverage <https://github.com/nedbat/coveragepy>`__ is checked.

   -  `coverage-badge <https://pypi.org/project/coverage-badge/>`__ is
      currently locally generated for use in ``README.rst``.

-  Documentation is generated with 
   `sphinx <https://github.com/sphinx-doc/sphinx>`__

   -  Documentation theme is `sphinx-rtd-theme
      <https://github.com/readthedocs/sphinx_rtd_theme>`__.

   -  Hosted on ``ReadTheDocs``

      -  Requires user setup at https://readthedocs.org/

Template Development
--------------------

Run tests for the template with:

.. code:: bash

   # Install with poetry
   poetry install
   # Run tests
   poetry run nox --session test # -- optional posargs to limit testing

Testing uses another, scaffolded Python project in ``./test_template/``
directory.
