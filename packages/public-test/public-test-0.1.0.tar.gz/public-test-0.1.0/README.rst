public-test
===========

Sample public project setup.

Usage
-----

Add the package to your dependencies. If you're working on a project managed by `poetry <https://python-poetry.org/>`_, use the following::

   $ poetry add public-test

If you're working on a project managed by `pipenv <https://pipenv.kennethreitz.org/>`_, use the following::

   $ pipenv install public-test

After that, you should be able to import the library in your Python code::

   from public_test import answer
   print(answer)

Development
-----------

This library itself is managed by `poetry <https://python-poetry.org/>`_. Read the docs for basic usage. You can run tests like this::

   $ poetry run pytest

To release a new version of the library, follow these steps:

#. Be sure to be on the ``master`` Git branch.
#. Decide whether your changes are `breaking, improvement, or a bug fix <https://semver.org/>`_. Use the poetry's `version command <https://python-poetry.org/docs/cli/#version>`_ to raise the version number.
#. Read the new number from the poetry's output and commit the change with ``git commit -am "release vX.Y.Z"``.
#. Tag the commit with ``git tag vX.Y.Z``
#. Release a new version by pushing it all to GitHub: ``git push origin master --tags``

The CI automatically builds the package and publishes it to the `PyPI <https://pypi.org/project/public-test/>`_. New releases get listed at `tags <https://github.com/digismoothie/django-toolbox/tags>`_. If you like your colleagues, for each release click on *Edit tag* and write a title and description (changelog).
