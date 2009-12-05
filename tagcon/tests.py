from django.test import TestCase
from django.template import Library, Template, Context, add_to_builtins,\
        TemplateSyntaxError, VariableDoesNotExist
import tagcon
register = Library()

class KeywordTag(tagcon.TemplateTag):

    limit = tagcon.IntegerArg(default=5)

    def render(self, context):
        self.resolve(context)
        return 'The limit is %d' % self.args.limit

class NoArgumentTag(tagcon.TemplateTag):

    def render(self, context):
        return 'No arguments here'


class ArgumentTypeTag(tagcon.TemplateTag):

    age = tagcon.IntegerArg()
    handle = tagcon.StringArg()

    def render(self, context):
        self.resolve(context)
        return '%s is %d' % (self.args.handle, self.args.age)

add_to_builtins(KeywordTag.__module__)
add_to_builtins(NoArgumentTag.__module__)
add_to_builtins(ArgumentTypeTag.__module__)


class TagCreationTests(TestCase):

    def test_no_args(self):
        """A tag with keyword arguments works with or without the argument"""

        self.assertEqual(Template('{% keyword limit 200 %}').render(Context()),
                         'The limit is 200')

        self.assertEqual(Template('{% keyword %}').render(Context()),
                         'The limit is %d' %
                         KeywordTag._keyword_args['limit'].default)

    def test_args_format(self):
        """keyword argument syntax is {% tag arg value %}"""
        self.assertRaises(TemplateSyntaxError,
                          Template,
                          '{% keyword limit=25 %}')

        self.assertRaises(TemplateSyntaxError,
                          Template,
                          "{% keyword limit='25' %}")

        # i can't remember which one (url perhaps?) but there was a tag that
        # worked with single quotes but not double quotes and so we check both
        self.assertRaises(TemplateSyntaxError,
                          Template,
                          '{% keyword limit="25" %}')

    def test_handle_args(self):
        """tags with no arguments take no arguments"""
        self.assertRaises(TemplateSyntaxError,
                          Template,
                          '{% no_argument limit 25 %}')

    def test_argument_type(self):
        """defining argument type has some effect"""

        render = lambda t: Template(t).render(Context())

        t = Template('{% argument_type age 101 handle "alice" %}')
        self.assertEqual(t.render(Context()), 'alice is 101')

        # IntegerArg.clean calls int(value) to convert "101" to 101
        t = Template('{% argument_type age "101" handle "alice" %}')
        self.assertEqual(t.render(Context()), 'alice is 101')

        # IntegerArg.clean will choke on the string
        self.assertRaises(tagcon.TemplateTagValidationError,
                          render,
                          '{% argument_type age "101b" handle "alice" %}')

        # will not find a var named alice in the context
        try:
            render('{% argument_type age "101" handle alice %}')
        except TemplateSyntaxError, e:
            self.assertTrue(isinstance(e.exc_info[1], VariableDoesNotExist))

