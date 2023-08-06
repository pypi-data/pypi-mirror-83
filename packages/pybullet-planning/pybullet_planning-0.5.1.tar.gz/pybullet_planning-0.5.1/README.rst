=================
pybullet_planning
=================

.. start-badges

.. image:: https://readthedocs.org/projects/pybullet-planning/badge/?version=latest
    :target: https://pybullet-planning.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


.. image:: https://travis-ci.com/yijiangh/pybullet_planning.svg?branch=dev
    :target: https://travis-ci.com/yijiangh/pybullet_planning
    :alt: Travis CI


.. image:: https://coveralls.io/repos/github/yijiangh/pybullet_planning/badge.svg?branch=dev
    :target: https://coveralls.io/github/yijiangh/pybullet_planning?branch=dev
    :alt: Coveralls


.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://github.com/yijiangh/pybullet_planning/blob/dev/LICENSE
    :alt: License MIT

.. end-badges

.. Write project description

**pybullet_planning** is a suite of utility functions to facilitate robotic planning related research on the `pybullet <https://github.com/bulletphysics/bullet3>`_ physics simulation engine. Planning research made easy.


Main features
-------------

* easy-to-use functions to connect with pybullet, tailored for task and motion planning research
* built-in implementations of standard motion planners, including PRM, RRT, biRRT, A* etc.


Getting Started
---------------

**pybullet_planning** can be installed using ``pip``:

::

    pip install pybullet_planning


.. note::

    On Windows, you may need to install
    `Microsoft Visual C++ 14.0 <https://www.scivision.co/python-windows-visual-c++-14-required/>`_.


Once the installation is completed, you can verify your setup.
Start Python from the command prompt and run the following:

::

    >>> import pybullet_planning


First Steps
---------------

* `Documentation <https://pybullet-planning.readthedocs.io>`_

Contributing
------------

We love contributions!

Check the `Contributor's Guide <./CONTRIBUTING.rst>`_
for more details.

Releasing this project
----------------------

Ready to release a new version of **pybullet_planning**? Here's how to do it:

* We use `semver <https://semver.org/>`_, i.e. we bump versions as follows:

  * ``patch``: bugfixes.
  * ``minor``: backwards-compatible features added.
  * ``major``: backwards-incompatible changes.

* Update the ``CHANGELOG.rst`` with all novelty!
* Ready? Release everything in one command:

::

    invoke release [patch|minor|major]
    # with -b to bump version

* Celebrate! 💃

PyBullet Resources
-------------------

* Github - https://github.com/bulletphysics/bullet3
* Quickstart - https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/
* Forum - https://pybullet.org/Bullet/phpBB3/
* Wordpress - https://pybullet.org/wordpress/
* Examples - https://github.com/bulletphysics/bullet3/tree/master/examples/pybullet/examples
* Bindings - https://github.com/bulletphysics/bullet3/blob/master/examples/pybullet/pybullet.c

Credits
-------------

    Caelan Reed Garrett. PyBullet Planning. https://pypi.org/project/pybullet-planning/. 2020.

This package was initiated and maintained by Caelan Garrett `@caelan <https://github.com/caelan>`_
and other `contributors <https://github.com/yijiangh/pybullet_planning/blob/dev/AUTHORS.rst>`_.
