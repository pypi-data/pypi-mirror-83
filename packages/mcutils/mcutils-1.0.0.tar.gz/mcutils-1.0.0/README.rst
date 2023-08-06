=======
mcutils
=======


.. image:: https://img.shields.io/pypi/v/mcutils.svg
        :target: https://pypi.python.org/pypi/mcutils

.. image:: https://img.shields.io/travis/macanepa/mcutils.svg
        :target: https://travis-ci.org/macanepa/mcutils

.. image:: https://readthedocs.org/projects/mcutils/badge/?version=latest
        :target: https://mcutils.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




mcutils open-source


* Free software: GNU General Public License v3
* Documentation: https://mcutils.readthedocs.io.


Features
--------

* Create easy and simple Menu cycles.
    * Title, Subtitle, Text
    * Options (list the different alternatives to choose from)
        * Submenus (Menu instance)
        * Functions (Menu_Function instance [must pass the arguments as \*args])
                * Retrieve Menu_Function returned value
    * Each menu is an instance from the Menu Class
    * Allows to return to previous menus (parent menu)
    * Controlled user input
* Error Handler
* Directory Manager
    * List files in directory
    * Filter through different file extensions
    * Open files with default application (cross-platform support)
    * Select Files
    * Delete Files
* Basic Logger


Future Features
---------------
* Logger System

Supported Versions
------------------
* Python 3.x

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
