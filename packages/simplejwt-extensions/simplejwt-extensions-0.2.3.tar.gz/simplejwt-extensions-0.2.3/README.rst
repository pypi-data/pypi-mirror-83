Simple JWT Extensions
=====================

Extensions for the `djangorestframework-simplejwt
<https://github.com/SimpleJWT/django-rest-framework-simplejwt/>`__ library.

Settings
--------

All pre-existing settings for djangorestframework-simplejwt are unchanged. The
following settings are added and can be set in your ``settings.py`` file:

.. code-block:: python

  # Django project settings.py

  ...

  SIMPLE_JWT = {
      ...
      'NEW_USER_CALLBACK': None,
  }

-------------------------------------------------------------------------------

NEW_USER_CALLBACK
  A dot path to a callable that is used if the identifier from the token does
  not match a user in the database. Receives the request and the identifier as
  arguments. Should return None to fail authentication or a User object to
  succeed. Will only be used by the JWTAuthentication backend.

Backends
--------

JWTTokenAuthentication
  Use this instead of the ``djangorestframework-simplejwt``
  ``JWTTokenAuthentication`` backend to take advantage of features added by
  this package.
