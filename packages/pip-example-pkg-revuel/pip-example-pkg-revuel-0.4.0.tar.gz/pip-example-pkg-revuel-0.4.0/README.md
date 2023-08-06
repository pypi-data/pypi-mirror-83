# Pip example package 

[![Build Status](https://travis-ci.org/revuel/pip-example-pkg-revuel.svg?branch=master)](https://travis-ci.org/revuel/pip-example-pkg-revuel) 
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=revuel_pip-example-pkg-revuel&metric=coverage)](https://sonarcloud.io/dashboard?id=revuel_pip-example-pkg-revuel)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=revuel_pip-example-pkg-revuel&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=revuel_pip-example-pkg-revuel)
[![PyPI version](https://badge.fury.io/py/pip-example-pkg-revuel.svg)](https://badge.fury.io/py/pip-example-pkg-revuel)

---

[Tutorial about how to distribute pip packages](https://packaging.python.org/tutorials/packaging-projects/)

## Raw CLI
**Dependencies**

`pip install --upgrade setuptools wheel`

`pip install --upgrade twine`

**Build**

`python setup.py sdist bdist_wheel`

**Upload**

`twine upload  dist/*`

---

Here a minion just to make this file more friendly

[<img src="https://upload.wikimedia.org/wikipedia/commons/f/fe/Minion_%28example%29.svg" width="100"/>](image.png)
