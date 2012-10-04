from __future__ import with_statement
from django import template
from django.utils import translation


register = template.Library()


class override(object):
    def __init__(self, language):
        self.language = language
        self.old_language = translation.get_language()

    def __enter__(self):
        if self.language:
            translation.activate(self.language)
        else:
            translation.deactivate_all()

    def __exit__(self, exc_type, exc_value, traceback):
        translation.activate(self.old_language)


class LanguageNode(template.Node):
    def __init__(self, nodelist, language):
        self.nodelist = nodelist
        self.language = language

    def render(self, context):
        with override(self.language.resolve(context)):
            output = self.nodelist.render(context)
        return output


@register.tag
def language(parser, token):
    """
    This will enable the given language just for this block.

    Usage::

        {% language "de" %}
            This is {{ bar }} and {{ boo }}.
        {% endlanguage %}

    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(
            "'%s' takes one argument (language)" % bits[0])
    language = parser.compile_filter(bits[1])
    nodelist = parser.parse(('endlanguage',))
    parser.delete_first_token()
    return LanguageNode(nodelist, language)
