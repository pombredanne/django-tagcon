=============
django-tagcon
=============

.. attention::
   Tagcon has been abandoned by its original author due to a lack of interest
   in further development.  Please see TTag_ for a fork of Tagcon that is
   actively developed.

.. _TTag: https://github.com/lincolnloop/django-ttag


Django-Tagcon is a template tag constructor library for Django.  It supports a
range of features to make writing template tags easier:

- Syntax modeled on Django's friendly syntaxes for models and forms

- Standardized argument handling — never write tag boilerplate again!

- Positional and optional arguments

- Required arguments and argument defaults

- Comma-separated sequence arguments (e.g., ``1, 2, 3``)

- Flag arguments (that take no value)

- Argument validation support (``clean`` methods similar to forms)

- Automatic tag naming based on the class name (with optional override)

- Automatic tag registration with the module's ``register`` Library

- Easy resolution of context variable arguments, including filters

- Support for yielding strings from the ``render`` method


Requirements
============

Django-Tagcon requires Python 2.5 and the latest formal release of Django
(1.2.3, at the time of writing).


Installation
============

Just drop ``tagcon.py`` somewhere on Python's module path.


Example
=======

A simple example with a single optional argument::

    from django.contrib.auth.models import User
    from django.template import Library
    import tagcon

    register = Library()

    class UserListTag(tagcon.TemplateTag):
        limit = tagcon.IntegerArg(default=10)

        def render(self, context):
            self.resolve(context)
            yield "<ul>"
            for user in User.objects.all()[:self.args.limit]:
                yield "<li>%s</li>" % (user.username,)
            yield "</ul>"

And then, in a template (after loading the library)::

    {% user_list %}

or::

    {% user_list limit 20 %}


History
=======

The idea for a new, less painfully verbose and more consistent template tag
syntax for Django came up a few years ago at the Lawrence Journal-World, where
Tom X. Tobin first implemented what he then called "newtags".  Newtags was a
modification of the template-handling code in the LJW's internal Django branch;
the syntax was modeled somewhat after Django's model syntax, as this seemed
like a natural fit.  As this was the Dark Age around Django 0.91, the
implementation was eventually abandoned and became impossibly out of sync with
upstream Django.

A few years later Tom found himself at The Onion, helping to expand and manage
a Django-based library that included an increasing number of template tags.  He
decided to again write a library for easier template tag construction — but
this time based upon modern Django, and implemented as a separate library.  The
Onion was gracious enough to allow the library to be MIT licensed.

Tom no longer works for The Onion, but continues to maintain the library.


To-Do
=====

Lots, including documentation and proper tests.  (This code *has* been used in
production at The Onion, for what that's worth.)  Unlike most other tools that
Tom worked on over time and never released for want of polishing, he figured it
was better to just push it out first and polish it later.

In particular, Tom is not entirely comfortable with the underscore syntax to
denote positional arguments; he's open to better ideas there.


Contributing
============

Just fork, hack, and point Tom to the branch (preferably on GitHub); if it
looks good, he'll gladly pull it in.

There's more information in the "Contributing" document regarding submissions
and style.  In particular, contributions *must* be in a Git repository Tom can
pull from; he doesn't accept patch files.


Contact
=======

- Tom X. Tobin <tomxtobin@tomxtobin.com>
- "tomxtobin" on GitHub
