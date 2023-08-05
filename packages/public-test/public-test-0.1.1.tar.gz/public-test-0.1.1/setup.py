# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['public_test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'public-test',
    'version': '0.1.1',
    'description': 'Sample public project setup',
    'long_description': 'public-test\n===========\n\nSample public project setup.\n\nUsage\n-----\n\nAdd the package to your dependencies. If you\'re working on a project managed by `poetry <https://python-poetry.org/>`_, use the following::\n\n   $ poetry add public-test\n\nIf you\'re working on a project managed by `pipenv <https://pipenv.kennethreitz.org/>`_, use the following::\n\n   $ pipenv install public-test\n\nAfter that, you should be able to import the library in your Python code::\n\n   from public_test import answer\n   print(answer)\n\nDevelopment\n-----------\n\nThis library itself is managed by `poetry <https://python-poetry.org/>`_. Read the docs for basic usage. You can run tests like this::\n\n   $ poetry run pytest\n\nTo release a new version of the library, follow these steps:\n\n#. Be sure to be on the ``master`` Git branch.\n#. Decide whether your changes are `breaking, improvement, or a bug fix <https://semver.org/>`_. Use the poetry\'s `version command <https://python-poetry.org/docs/cli/#version>`_ to raise the version number.\n#. Read the new number from the poetry\'s output and commit the change with ``git commit -am "release vX.Y.Z"``.\n#. Tag the commit with ``git tag vX.Y.Z``\n#. Release a new version by pushing it all to GitHub: ``git push origin master --tags``\n\nThe CI automatically builds the package and publishes it to the `PyPI <https://pypi.org/project/public-test/>`_. New releases get listed at `tags <https://github.com/digismoothie/django-toolbox/tags>`_. If you like your colleagues, for each release click on *Edit tag* and write a title and description (changelog).\n\nAutomatic Releases\n------------------\n\nFor the CI to be able to publish new releases to PyPI, a ``PYPI_TOKEN`` environment variable first needs to be set in the CircleCI project settings:\n\n#. Read the docs about `PyPI tokens <https://pypi.org/help/#apitoken>`_ and `CircleCI project environment variables <https://circleci.com/docs/2.0/env-vars/#setting-an-environment-variable-in-a-project>`_.\n#. Generate a token at your `PyPI account settings <https://pypi.org/manage/account/token/>`_. Copy the token and treat it as a secret.\n#. Go to CircleCI project settings, section *Environment Variables*, and add a new one called ``PYPI_TOKEN``. Paste the token as a value.\n',
    'author': 'Digismoothie s.r.o.',
    'author_email': 'info@digismoothie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digismoothie/public-test',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
