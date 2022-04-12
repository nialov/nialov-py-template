Documentation for nialov-py-template
====================================

This is a `copier <https://github.com/copier-org/copier>`__ template for
Python ``3.8+`` development.

Highly opinionated and made for personal use.

Short description of functionality
----------------------------------

-  Testing framework based on `doit <https://github.com/pydoit/doit>`__
   and `nox <https://github.com/theacodes/nox>`__.

   -  Allows replication of continuous integration (=ci) tests locally.

   -  Continuous integration is conducted with ``GitHub Actions``.

   -  Continuous integration tasks are replicable locally with ``doit``
      tasks defined in ``dodo.py``.

      -  Note that ``docs`` are hosted on ``ReadTheDocs``, the task is only
         ran in ci to test the building with task that mimics ``ReadTheDocs``.

      -  An
         `action <https://github.com/pypa/gh-action-pypi-publish>`__ exists
         that will push to PyPI on tagged commits.

         -  However this requires a ``PYPI_PASSWORD`` API token to work.

         -  See end of ``doit`` job in workflow file.

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

Run tests for the template with ``poetry`` or ``nix + poetry``:

-  With ``nix + poetry``:

.. code:: bash

   # With nix (installs all development dependencies automatically)
   # But one dependency is poetry which is used for actual python
   # dependency management. Therefore poetry install is required to install
   # python dependencies.
   nix develop -c poetry install
   # After python dependencies (including nox) are installed, nox can be ran
   # to run the template tests.
   nix develop -c poetry run nox

-  With ``poetry``:

.. code:: bash

   poetry install
   poetry run nox

Testing uses another, scaffolded Python project in ``./test_template/``
directory. To run tests for supported Python version 3.8 and 3.9 you
need to have them installed on your system if you do not use ``nix``.
