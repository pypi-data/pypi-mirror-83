pyramid_csrf_multi_scheme
=========================

.. image:: https://github.com/jvanasco/pyramid_csrf_multi_scheme/workflows/Python%20package/badge.svg
        :alt: Build Status

This package enables two separate cookie tokens on each request, bound to the scheme:

* a SECURE HTTPS only cookie
* a mixed-use insecure http token (which is also available on https).

If the current scheme is `HTTPS`:

* only the SECURE HTTPS token will be considered
* HOWEVER calls to generate a new token will reset both the SECURE HTTPS and the
  insecure http tokens.

If the current scheme is `insecure http`:

* the SECURE HTTPS tokens are ignored as they are not even available, and only the
  insecure http token is considered.


Python Versions
---------------

This package is currently supported under Python2.7 and 3.8; other 3.x versions may work.


Why?
----

If an application supports both `HTTP` and `HTTPS` endpoints, this package simplifies
isolating the CSRF data from both.


Is this necessary?
------------------

I'm not sure, but have decided to err on the side of caution.

HTTP traffic is sent in plaintext and capable of being intercepted by a
man-in-the-middle or network packet sniffing.

It seems plausible that someone might read a csrf token via HTTP and use that
in attempts to compromise HTTPS endpoints in a mixed use environment.

A better option is to only use HTTPS tokens and forms - but that is not
always an option.


debugtoolbar support!
---------------------

just add to your `ENVIRONMENT.ini` file, or similar application configuration.

.. code-block:: python

    debugtoolbar.includes = pyramid_csrf_multi_scheme.debugtoolbar

Tthe debugtoolbar will now have a `CSRFMultiScheme` panel that has the following info:

* configuration info on the cookie names
* incoming request csrf values
* outgoing response csrf values


License
-------

Most of this is just code lightly edited from Pyramid, and
therefore available under Pyramid's licensing terms.

