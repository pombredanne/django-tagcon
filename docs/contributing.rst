============
Contributing
============

I gladly take contributions of code, documentation, and tests.

Please note that contributions must be in a Git repository that I can pull
from; I don't accept patch files of any sort.  (This *is* the 21st century,
right?)  ^_^  I prefer repositories hosted on GitHub, but that's not required.


Style guide
===========

- Follow Django's style guide in "Contributing" unless contradicted here.

- Always separate top-level function and class definitions with two blank
  lines, as per PEP8.  (Django seems to ignore this everywhere.)

- Always use multiline docstrings with opening triple quotes (``"""``) on their
  own line, followed by a one-line summary on the next line, and then (if there
  is more) a blank line followed by the remainder of the docstring text.  Close
  the docstring with triple quotes on their own line.  *Don't* leave a blank
  line between the last line of text and the closing quotes.

  In other words, do this::

      def some_function(foo):
         """
         This is a docstring.
         """
         return True

      def another_function(bar):
          """
          This is an extended docstring.

          Docstrings are good to have!
          """
          return False

  and *not* this::

      def some_function(foo):
          "This is a docstring."
          return True

      def another_function(bar):
          """This is an extended docstring.

          Docstrings are good to have!

          """
          return False

- All documentation and comments are in American English, with `Garner's Modern
  American Usage` as the style guide I try to adhere to.  (Don't worry if
  you're not familiar with it; I'll handle copy editing.)

  A couple of exceptions to note:

  - I write "email" without a hyphen; "e-mail" (with a hyphen) looks ridiculous
    to me, and I won't tolerate it.  ;)

  - Quotations follow "logical" precedence for punctuation, meaning that (for
    instance) a trailing period is inside or outside the quotes depending on
    whether it belongs to the quoted text.  (Wikipedia also uses the same
    style for quotes.)
