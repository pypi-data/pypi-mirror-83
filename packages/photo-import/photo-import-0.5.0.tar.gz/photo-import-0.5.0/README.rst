============
Photo Import
============

A tool for importing photos from one directory into a hierarchical
folder structure in another directory based on the EXIF data of the
photos.

The idea is that you're able to sort a folder full of photos (such as
those straight off a memory card) into a navigable hierarchy like the
following:

.. code:: bash

   $ tree Photos
   Photos
   └── 2019
       ├── 03
       │   ├── 11
       │   │   ├── photo1.jpg
       │   │   ├── photo2.jpg
       │   │   └── photo3.jpg
       │   ├── 12
       │   │   └── photo4.jpg
       │   └── 13
       └── 04
           └── 01
               ├── photo5.jpg
               └── photo6.jpg

----------
Usage
----------

Installation
============

The ``photo-import`` command can be installed via ``pip`` as follows:

.. code:: bash

   $ pip install photo-import
   $ photo-import --version
   0.3.0

Usage
==========

Basic usage is as follows:

.. code:: bash

   $ photo-import /path/to/source/image.jpg /path/to/sorted/photos/

This will move ``image.jpg`` into an appropriate folder within the
``/path/to/sorted/photos/`` directory, resulting in, for example,
``/path/to/sorted/photos/2019/03/11/image.jpg``.

.. code:: bash

   $ photo-import /path/to/photo-source /path/to/sorted/photos/

This will move  all photos found within the ``/path/to/photo-source``
directory into an appropriate folder within the
``/path/to/sorted/photos/`` directory, resulting in, for example,
``/path/to/sorted/photos/2019/03/11/image.jpg``.

Further usage instructions are provided by using the ``--help`` option:

.. code:: bash

   $ photo-import --help


-----------
Development
-----------

Running from source
===================

There's also a "runner" python script provided in the root of this
repository for convenience when the source code is checked out locally:

.. code:: bash

   $ pip install -r requirements.txt
   $ python runner.py --version
   0.3.0
   $ ./runner.py --version
   0.3.0

Commit message format
=====================

Commit messages should conform to the `conventional commits`_ standard, and to
help with this you should install the `commitizen`_ tool:

.. code:: bash

   $ pip install -r dev-requirements.txt
   $ git add .
   $ cz commit

Tests
==========

To run the test suite locally, use ``nose2`` for unit tests, and ``behave`` for
behavioural tests (Note that running behave will run
``python setup.py install``, installing ``photo-import`` into your current
environment):

.. code:: bash

   $ pip install -r requirements.txt
   $ nose2
   $ behave

.. _conventional commits: https://www.conventionalcommits.org/en/
.. _commitizen: https://pypi.org/project/commitizen/
