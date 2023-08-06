.. contents::

Introduction
============

Menu package for cpskin


Warning
=======

This package depends on cpskin.theme but does not install the theme automatically except in tests.

You better have to install the cpskin.theme via "control panel/theme"


Tests
=====

This package is tested using Travis CI. The current status is :

.. image:: https://travis-ci.org/IMIO/cpskin.menu.png
    :target: http://travis-ci.org/IMIO/cpskin.menu


Robot tests
===========


Run all tests
-------------

bin/test


Run specific tests
------------------

You can launch the robot server with the command:

    bin/robot-server cpskin.menu.testing.CPSKIN_MENU_ROBOT_TESTING

And launch the tests:

    bin/robot cpskin/menu/tests/robot/<yourfile>.robot

You can sandbox on http://localhost:55001/plone/
