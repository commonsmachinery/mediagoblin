.. MediaGoblin Documentation

   Written in 2011, 2012 by MediaGoblin contributors

   To the extent possible under law, the author(s) have dedicated all
   copyright and related and neighboring rights to this software to
   the public domain worldwide. This software is distributed without
   any warranty.

   You should have received a copy of the CC0 Public Domain
   Dedication along with this software. If not, see
   <http://creativecommons.org/publicdomain/zero/1.0/>.

.. _configuration-chapter:

========================
Configuring MediaGoblin
========================

If you have successfully installed MediaGoblin and have a running, if
generic, instance; you'll want to make several customizations. This
document provides an overview of available customization options and
processes.

MediaGoblin's Configuration Files
=================================

To configure MediaGoblin, you will want to maintain versions of the
following files with local modifications. These files are:

``mediagoblin.ini``
-------------------

This is the main configuration file for the MediaGoblin application.
MediaGoblin reads all settings from this file. To tweak the behavior
and operation of MediaGoblin, you will want to edit this file.

``paste.ini``
-------------

This is the server configuration file, for the Python/WSGI
components.

See:

- `paste deploy <http://pythonpaste.org/deploy/>`_, and

- `paste script <http://pythonpaste.org/script/>`_.

ignorable, save for configuration sessions configure
``paste.ini`` also configures some middleware that you will not need
to edit except to configure sessions.

.. todo:: insert link here to the documentation of session
          configuration.

If you are adding a Python server other than FastCGI or plain HTTP,
you would configure that service here. Beyond these uses, you will not
need to change ``paste.ini`` much.

``mediagoblin/config_spec.ini``
-------------------------------

You will not need to edit ``mediagoblin/config_spec.ini`` file unless
your actually patching the core MediaGoblin codebase. Nevertheless,
this file provides a useful reference.

``mediagoblin/config_spec.ini`` is a specification for mediagoblin.ini
itself as a configuration file. It defines types and defaults for
configuration values in ``mediagoblin.ini``. This is the canonical
reference for all configuration values, including (unintentionally)
hidden or obscured options.

Making Local Copies
===================

Given a :ref:`vitrualenv configuration <installing-with-virtualenv>`,
to make local configuration changes, use the following procedure:

To change values set in ``mediagoblin.ini``, create a local copy named
``mediagoblin_local.ini`` as follows: ::

    cp mediagoblin.ini mediagoblin_local.ini

Then, edit ``mediagoblin_local.ini`` as needed. After changing this
file you may need to restart your application server for the changes
to take effect.

To change values set in ``paste.ini``, create a local copy named
``paste_local.ini`` as follows: ::

    cp paste.ini paste_local.ini

Then, edit ``paste_local.ini`` as needed. After changing this file you
may need to restart your application server for the changes to take
effect. The MediaGoblin commands and software will always read local
configuration files first and use values set there rather than the
default values.

.. note::

   All commands provide a way to pass in a specific config file,
   usually with the ``-cf`` flag.

Common Configuration Modifications
==================================

Enable Email Notifications
--------------------------

Most deployments will need to configure email sending. During
development, MediaGoblin runs in an "email debug mode." To make
MediaGoblin send email itsef, you need a mailer daemon.

Change the following value in your ``mediagoblin_local.ini`` file: ::

    email_debug_mode = false

Modify the "from" email address by setting ``email_sender_address``,
as in the following example: ::

    email_sender_address = "foo@example.com"

Depending on your email configuration you may also need to configure
the following optional settings:

- ``email_smtp_host``
- ``email_smtp_port``
- ``email_smtp_user``
- ``email_smtp_pass``

Additional Configuration
------------------------

.. todo:: provide better configuration documentation (possibly in a
          reference section.)

There are many undocumented configuration options as of |release|.

If you need to configure or modify your MediaGoblin instance, hop
onto IRC and we'll help you out:

.. pull-quote::

   ``#mediagoblin`` on ``irc.freenode.net``

Celery
======

Celery is the job queuing system that MediaGoblin uses to manage
transcoding and image manipulation work.

.. admonition:: Coming soon...

   A Celery-specific configuration section.
