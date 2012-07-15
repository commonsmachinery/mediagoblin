.. MediaGoblin Documentation

   Written in 2011, 2012 by MediaGoblin contributors

   To the extent possible under law, the author(s) have dedicated all
   copyright and related and neighboring rights to this software to
   the public domain worldwide. This software is distributed without
   any warranty.

   You should have received a copy of the CC0 Public Domain
   Dedication along with this software. If not, see
   <http://creativecommons.org/publicdomain/zero/1.0/>.

.. _codebase-chapter:

========================
 Codebase Documentation
========================

.. contents:: Sections
   :local:


This chapter covers the libraries that GNU MediaGoblin uses as well as
various recipes for getting things done.

.. Note::

   This chapter is in flux.  Clearly there are things here that aren't
   documented.  If there's something you have questions about, please
   ask!

   See `the join page on the website <http://mediagoblin.org/join/>`_
   for where we hang out.

For more information on how to get started hacking on GNU MediaGoblin,
see `the wiki <http://wiki.mediagoblin.org/>`_.


Software Stack
==============

* Project infrastructure

  * `Python <http://python.org/>`_: MediaGoblin is written in Python,
    and supports the 2.6 and 2.7 series of Python.

  * `Nose <http://somethingaboutorange.com/mrl/projects/nose/>`_: The
    unit testing framework.

  * `virtualenv <http://www.virtualenv.org/>`_: (*Optional.*) Creates
    an isolated environment for MediaGoblin and its
    dependencies. [#virtualenv-note]_

* Data storage

  * `SQLAlchemy <http://sqlalchemy.org/>`_: SQL ORM and database
    interaction library for Python.

  * Database: Currently MediaGoblin supports SQLite and PostgreSQL
    backends.

* Web application

  * `Paste Deploy <http://pythonpaste.org/deploy/>`_ and `Paste Script
    <http://pythonpaste.org/script/>`_: Used for configuring and
    launching the application.

  * `WebOb <http://pythonpaste.org/webob/>`_: Provides an
    interface/abstraction for HTTP requests and WSGI.

  * `Routes <http://routes.groovie.org/>`_: Used for URL routing.

  * `Beaker <http://beaker.groovie.org/>`_: Provides session handling
    and caching.

  * `Jinja2 <http://jinja.pocoo.org/docs/>`_: The template engine.

  * `WTForms <http://wtforms.simplecodes.com/>`_: Provides validation,
    handling, and abstraction handling, for HTML forms.

  * `Celery <http://celeryproject.org/>`_: Provides task queuing for
    potentially long running tasks like resizing images, and encoding
    video and audio.

  * `Babel <http://babel.edgewall.org>`_: Used to extract and compile
    translations.

  * `Markdown (for python) <http://pypi.python.org/pypi/Markdown>`_:
    implementation of `Markdown <http://daringfireball.net/projects/markdown/>`_
    text-to-html tool to make it easy for people to write rich-text
    comments, descriptions, and etc.

  * `lxml <http://lxml.de/>`_: For xml and html processing in Python.

* Media processing libraries:

  * `Python Imaging Library <http://www.pythonware.com/products/pil/>`_:
    Used to re-size and otherwise convert images for display.

  * `GStreamer <http://gstreamer.freedesktop.org/>`_: (*Optional.*),
    Used to transcode video and audio. Only required if your
    MediaGoblin instance will support audio and video.

  * `chardet <http://pypi.python.org/pypi/chardet>`_: (*Optional.*)
    Used to make ascii art thumbnails. Only required if your
    MediaGoblin instance will support ascii art.

* Front end:

  * `JQuery <http://jquery.com/>`_: for groovy JavaScript things


.. [#virtualenv-note] If you install MediaGoblin from distribution packages
   you may not need to use virtualenv.


Codebase Organization
=====================

After checking out the MediaGoblin code base, you'll find the
following directory tree: ::

    mediagoblin/
    |- mediagoblin/              # source code
    |  |- tests/
    |  |- templates/
    |  |- auth/
    #  |-                        # more directories here.
    |  \- submit/
    |- docs/                     # documentation
    |- devtools/                 # some scripts for developer convenience

All the code for GNU MediaGoblin is in the
``mediagoblin/mediagoblin/`` directory.


When you create the virtual environmnet (virtualenv), your
``mediagoblin/`` folder will have the following directories: ::

    |- bin/                      # scripts
    |- develop-eggs/
    |- lib/                      # python libraries installed into your virtualenv
    |- include/
    |- mediagoblin.egg-info/
    |- parts/
    |- user_dev/                 # sessions, etc


Within the source directory, the following three files contain key
components of the package:

``routing.py``
   Maps url paths to views

``views.py``
   Handles http requests.

``models.py``
   Holds the data model for SQLalchemy. These are all of the
   MediaGoblin data structures.

There are several sub-directories of ``mediagoblin/``: tests,
templates, auth, submit, and so forth. While you can discover the
purpose of these modules from reading the code itself, in general:

- ``tests`` holds code for the unit tests.

- ``templates`` holds all the templates for the output.

- ``auth`` and ``submit`` are modules that enacpsulate authentication
   and media item submission.

If you look in most of these directories, you'll see they have their
own ``routing.py``, ``view.py``, and ``models.py`` files in addition
to other code.
