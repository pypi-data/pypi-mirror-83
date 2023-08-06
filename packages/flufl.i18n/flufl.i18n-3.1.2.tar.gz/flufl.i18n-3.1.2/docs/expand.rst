===================
Expanding templates
===================

.. currentmodule:: flufl.i18n

The Python standard library defines :class:`string.Template` strings, which
are the implementation of `PEP 292`_ simple string templates.  With template
strings substitution variables are identified by a leading ``$``-sign [#]_.  A
substitution dictionary names the keys and values that should be interpolated
into the template, replacing the variables.  This module defines the
:meth:`expand()` function which takes the translated string and a substitution
dictionary, and returns the resulting string.

Normally though, you shouldn't have to call this function yourself.
::

    >>> key_1 = 'key_1'
    >>> key_2 = 'key_2'

    >>> from flufl.i18n import expand
    >>> # This may fail for Python < 2.6.5
    >>> print(expand(
    ...     '$key_2 is different than $key_1', {
    ...         key_1: 'the first key',
    ...         key_2: 'the second key',
    ...         }))
    the second key is different than the first key


.. _`PEP 292`: http://www.python.org/dev/peps/pep-0292/

.. [#] See the :class:`string.Template` documentation for the complete set of
       rules.
