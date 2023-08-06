.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=========================
visaplan.zope.inputmacros
=========================

Generic METAL_ macros for input fields

This package uses the TAL_ / METAL_ XML-based template language introduced by
Zope_ to provide simple input fields from Python dictionaries,
without any connection to schema data whatsoever.

The fields (or, more precisely: field sets) are created with classes for the
Bootstrap_ grid layout system.


Features
--------

- Input elements for `Horizontal forms`_
- `readonly` fields
- `required` fields
- labels


Examples
--------

This add-on is currently under development and not yet used on public internet
sites.


Documentation
-------------

After installing, you may try the view

- formfields_div_

in your Zope instance; the macros are "self-documenting".

*Note:* Currently it helps to understand German;
this view is not (yet?) internationalized.

The macros, however, are language-agnostic;
the don't provide any texts by themselves but use what you throw at them.


Installation
------------

If you use the macros in your own Plone add-on, add it to the dependencies,
e.g. in the setup.py file::

    setup(...,
        install_requires=[
            ...,
            'visaplan.zope.inputmacros',
            ],
        ...)


Or install ``visaplan.zope.inputmacros`` by adding it to your buildout::

    [buildout]
    ...
    eggs =
        visaplan.zope.inputmacros


and then running ``bin/buildout``


Requirements
------------

- You'll need a language interpreter as well; this will be given in default
  Zope / Plone installations.
  We don't specify this here to allow you to choose your own.

  Starting with Plone 5, Chameleon_ with the z3c.pt_ compatiblily layer is used;
  this should work as well.

- To make use of the classes applied to the HTML elements, you'll need
  `Bootstrap 3`_; you may use

  - collective.js.bootstrap_,
    perhaps via
  - plonetheme.bootstrap_.

  Bootstrap 4 might work as well, but we didn't try (yet).

- The use of Bootstrap 3 implies the need for jQuery 1.11.2;
  with Plone 4, you'd probably use plone.app.jquery_ 1.11.2+.


Contribute
----------

- Issue Tracker: https://github.com/visaplan/zope.inputmacros/issues
- Source Code: https://github.com/visaplan/zope.inputmacros


Support
-------

If you are having issues, please let us know;
please use the `issue tracker`_ mentioned above.


License
-------

The project is licensed under the GPLv2.

.. _`issue tracker`: https://github.com/visaplan/zope.inputmacros/issues
.. _Bootstrap: https://getbootstrap.com
.. _`Bootstrap 3`: https://getbootstrap.com/docs/3.3/migration/
.. _Chameleon: https://pypi.org/project/Chameleon/
.. _collective.js.bootstrap: https://pypi.org/project/collective.js.bootstrap
.. _formfields_div: http://localhost:8080/Plone/formfields_div
.. _`Horizontal forms`: https://getbootstrap.com/docs/3.3/css/#forms-horizontal
.. _METAL: https://en.wikipedia.org/wiki/Template_Attribute_Language#METAL
.. _plone.app.jquery: https://pypi.org/project/plone.app.jquery
.. _plonetheme.bootstrap: https://pypi.org/project/plonetheme.bootstrap
.. _TAL:  https://en.wikipedia.org/wiki/Template_Attribute_Language
.. _Zope: https://pypi.org/project/Zope/
.. _z3c.pt: https://pypi.org/project/z3c.pt

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
