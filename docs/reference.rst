=======================
django-tagcon reference
=======================


Overview
========

Django-Tagcon replaces the normal method of creating custom template tags.  It
uses a custom template ``Node`` subclass, ``TemplateTag``, which handles all of
the relevant aspects of a tag: defining and parsing arguments, handling
validation, resolving variables from the context, and rendering output.  It
tries to make the most common cases extremely simple, while making even complex
cases easier than they would be otherwise.

``TemplateTag`` and the various ``Arg`` classes are consciously modeled after
Django's ``Model``, ``Form``, and respective ``Field`` classes.  ``Arg``s are
set on a ``TemplateTag`` in the same way ``Field``s would be set on a
``Model`` or ``Form``.


TemplateTag
===========

A minimal ``TemplateTag`` might look like this::

    from django.template import Library
    import tagcon

    register = Library()

    class CustomTag(tagcon.TemplateTag):
        def render(self, context):
            return "Hi there!"

This would create a tag ``{% custom %}`` which took no arguments and rendered
``Hi there!``.  Tag naming is automatically based off of the class name, but
can be overridden (see the ``Meta`` options below).  The library can likewise
be explicitly specified, but in most cases automatically using the module's
``register`` library will do what is wanted anyway.


Meta options
------------

A ``TemplateTag`` can take various options via a ``Meta`` inner class::

    class FoobarTag(tagcon.TemplateTag):
        class Meta:
            name = "special"

        def render(self, context):
            return "Yes, I'm special."

This would create a tag ``{% special %}``, rather than ``{% foobar %}``.

The various ``Meta`` options follow.


name
~~~~

As shown above, ``name`` lets you explicitly choose a name for your tag.  If
``name`` is not given, the tag's name will be created by taking the class's
name and converting it from CamelCase to under_score format, with any trailing
``Tag`` in the class name ignored.  Thus ``KittyCatTag`` would become.
``{% kitty_cat %}``, and ``AmazingStuff`` would turn into
``{% amazing_stuff %}``.


library
~~~~~~~

Explicitly specify a library to register this tag with.  As long as the tag is
defined in a normal tag module with a ``register = Library()`` line, this
shouldn't be necessary.


silence_errors
~~~~~~~~~~~~~~

Whether to ignore exceptions raised by the tag, returning the settings'
``TEMPLATE_STRING_IS_INVALID`` string or ``''``.  This is ``False`` by default
at the moment, although this may change.


render
------

A ``render`` method must be added to any ``TemplateTag`` subclass, and takes a
template ``context`` as a required argument.  This is where the logic for your
tag would typically take place.  ``render`` must return a string *or* yield
strings as a generator.  If your tag doesn't return anything (e.g., it only
manipulates the context), ``render`` can simply return an empty string.

Yielding strings from ``render`` (using ``yield``) will work just as if those
strings were joined without separators (e.g., via ``''.join``) before being
returned; the tag will join the output for you automatically.

To use the values of the tag's arguments, if any, you must first call the
following method inside ``render``::

    self.resolve(context)

This will perform any context resolution if necessary, and populate the tag's
``args`` dictionary with the values of the tag's arguments.  ``args`` is a
special dictionary that also allows key lookup via attribute access, e.g.,
``self.args.somevar`` is the same as ``self.args['somevar']``.


Arguments
---------

Arguments can be either positional or keyword.


Keyword arguments
~~~~~~~~~~~~~~~~~

Keyword arguments can appear in any order in a tag's arguments, after the
positional arguments.  They are specified as follows::

    class KeywordTag(tagcon.TemplateTag):
        limit = tagcon.Arg()
        offset = tagcon.Arg()

This would create a tag named ``keyword`` which took two optional arguments,
``limit`` and ``offset``.  They could be specified in any order::

    {% keyword %}

    {% keyword limit 10 %}

    {% keyword offset 25 %}

    {% keyword limit 15 offset 42 %}

    {% keyword offset 4 limit 12 %}

The values for arguments are available in the tag's ``args`` attribute after
``self.resolve(context)`` is called in ``render``.  In the above example,
``self.args.limit`` would have the value of the ``limit`` argument, and
``self.args.offset`` would have the value of ``offset``; if either was not
given, the value would be ``None``.  (Default values can be changed; see the
Args section below.)


Positional arguments
~~~~~~~~~~~~~~~~~~~~

Positional arguments are given via a single underscore, like this::

    class PositionalTag(tagcon.TemplateTag):
        _ = (
            tagcon.Arg('first'),
            tagcon.Arg(name='second'),
        )

This would result in a tag named ``positional`` which took two required
arguments, which would be assigned to ``self.args.first`` and
``self.args.second`` after ``resolve`` is called.

Positional arguments *must* take a ``name`` argument, as they do not have a
keyword to create the variable name from.  (``name`` is the first argument to
``Arg``, so the keyword can be omitted as shown with ``first`` above.)

Positional arguments can also take required strings for readability's sake::

    class RangeTag(tagcon.TemplateTag):
        _ = (
            tagcon.Arg('start'),
            'to',
            tagcon.Arg('finish'),
        )

This would create a tag named ``range`` which would take three arguments, the
second of which must be the string ``to``.

If only a single positional argument is present, it can be written like this::

    class SinglePositionalArgTag(tagcon.TemplateTag):
        _ = tagcon.Arg('onlyarg')

This is the same as specifying::

    class SinglePositionalArgTag(tagcon.TemplateTag):
        _ = (
            tagcon.Arg('onlyarg'),
        )

Argument Types
==============

Arg and its subclasses provide various other levels of parsing and validation.


Arg
---

This is the base class for all other argument types.  Behavior can be defined
via the following constructor arguments.


name (default first argument, uses the keyword if not specified)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the name which the value will be stuffed into in ``self.args``.  It is
*not* the keyword name used in the tag itself.


required (defaults to False)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Whether the argument is required.  Positional arguments are implicitly required.


default (defaults to None)
~~~~~~~~~~~~~~~~~~~~~~~~~~

The default value for this argument if it is not specified.


resolve (defaults to true)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Whether to resolve the argument as a template variable if it is not a
literal. (surrounded by single or double quotes).  You will have to call
``self.resolve(context)`` in your ``render`` for this to take effect.


multi (defaults to False)
~~~~~~~~~~~~~~~~~~~~~~~~~

Whether the argument's value may consist of multiple comma-separated items
(which can be resolved or not depending on the value of ``resolve``).


flag (defaults to False)
~~~~~~~~~~~~~~~~~~~~~~~~

Denotes a keyword argument that does *not* have an associated value.  Its value
is ``True`` if the keyword is given, and ``False`` otherwise.


IntegerArg
----------

Validates that the argument is an integer, otherwise throws a template error.


StringArg
---------

Validates that the argument is a ``string`` instance, otherwise throws a
template error.


DateTimeArg
-----------

Validates that the argument is a ``datetime`` instance, otherwise throws a
template error.


DateArg
-------

Validates that the argument is a ``date`` instance, otherwise throws a template
error.


TimeArg
-------

Validates that the argument is a ``time`` instance, otherwise throws a template
error.


ModelInstanceArg
----------------

This ``Arg`` subclass validates that the passed in value is an instance of the
specified ``Model`` class.  It takes a single named argument, ``model``.  Note
that ModelInstanceArgs cannot take multiple values using ``multi``.


model (required)
~~~~~~~~~~~~~~~~

Argument is the ``Model`` class you want to validate against.  An error will be
thrown if the argument value is not an instance of this ``Model`` class.


Full Example
============

This example provides a template tag which outputs a tweaked version of the
instance name passed in.  It demonstrates using the various Arg types to have
tagcon do the hard work for you::

    class TweakName(tagcon.TemplateTag):
        """
        Provides the tweak_name template tag, which outputs a
        slightly modified version of the NamedModel instance passed in.

        {% tweak_name instance [offset=0] [limit=10] [reverse] %}
        """

        _ = (tagcon.ModelInstanceArg('instance', model=NamedModel))
        offset = tagcon.IntegerArg(default=0)
        limit = tagcon.IntegerArg(default=10)
        reverse = tagcon.Arg(flag=True)

        def render(self, context):
            self.resolve(context)

            name = self.args.instance.name

            # reverse if appropriate
            if self.args.reverse:
                name = name[::-1]

            # check that limit is not < 0
            if self.args.limit < 0:
                raise tagcon.TemplateTagValidationError("limit must be >= 0")

            # apply our offset and limit
            name = name[self.args.offset:][0:self.args.limit]

            # return the tweaked name
            return name

Example usages::

    {% tweak_name inst limit 5 %}

    {% tweak_name inst offset 1 %}

    {% tweak_name inst reverse %}

    {% tweak_name inst offset 1 limit 5 reverse %}
