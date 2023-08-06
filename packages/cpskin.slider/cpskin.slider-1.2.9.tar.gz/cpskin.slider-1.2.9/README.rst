.. contents::

Introduction
============

`FlexSlider <http://www.woothemes.com/flexslider/>`_ integration into Plone.

This package adds a "Slider view" on Collections that displays the collection
results in a slider.

There is also a Slider portlet that can be added to your site.

Note that the slider is displaying the Plone image field of News items but
does also work with `collective.contentleadimage <https://github.com/collective/collective.contentleadimage>`_
for all other content types without additional configuration.


Tests
=====

This package is tested using Travis CI. The current status is :

.. image:: https://travis-ci.org/IMIO/cpskin.slider.png
    :target: http://travis-ci.org/IMIO/cpskin.slider


Robot tests
===========


Run all tests
-------------

bin/test


Run specific tests
------------------

You can launch the robot server with the command:

    bin/robot-server cpskin.slider.testing.CPSKIN_SLIDER_ROBOT_TESTING

And launch the tests:

    bin/robot cpskin/slider/tests/robot/<yourfile>.robot

You can sandbox on http://localhost:55001/plone/
