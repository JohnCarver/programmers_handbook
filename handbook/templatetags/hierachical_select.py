from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

# TODO add selecting of the current node
@register.filter(needs_autoescape=True)
def hierachical_select_options(nodes, autoescape=None):
    string = ''
    for node in nodes:
        string += _get_optionhierachy(node, '', autoescape)
    return mark_safe(string)


def _get_optionhierachy(node, indent, autoescape):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    string = '<option value="%i">%s %s (%s)</option>' % (node.id, indent, esc(node.title), esc(node.slug))
    for child in node.get_children():
        string += _get_optionhierachy(child, '-' + indent, autoescape)
    return mark_safe(string)
