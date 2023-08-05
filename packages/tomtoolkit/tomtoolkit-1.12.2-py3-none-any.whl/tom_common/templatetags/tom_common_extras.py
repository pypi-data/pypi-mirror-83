from django import template
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.conf import settings
from django_comments.models import Comment
from guardian.shortcuts import get_objects_for_user

register = template.Library()


@register.simple_tag
def comments_enabled():
    """
    Returns the TOM setting specifying whether or not comments are enabled
    """
    try:
        return settings.COMMENTS_ENABLED
    except AttributeError:
        return True


@register.simple_tag
def verbose_name(instance, field_name):
    """
    Displays the more descriptive field name from a Django model field
    """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.inclusion_tag('comments/list.html', takes_context=True)
def recent_comments(context, limit=10):
    """
    Displays a list of the most recent comments in the TOM up to the given limit, or 10 if not specified.

    Comments will only be displayed for targets which the logged-in user has permission to view.
    """
    user = context['request'].user
    targets_for_user = get_objects_for_user(user, 'tom_targets.view_target')

    # In django-contrib-comments, the Comment model has a field ``object_pk`` which refers to the primary key
    # of the object it is related to, i.e., a comment on a ``Target`` has an ``object_pk`` corresponding with the
    # ``Target`` id. The ``object_pk`` is stored as a TextField.

    # In order to filter on ``object_pk`` with an iterable of ``IntegerFields`` using the ``in`` comparator,
    # we have to cast the ``object_pk`` to an int and annotate it as ``object_pk_as_int``.
    return {
        'comment_list': Comment.objects.annotate(
            object_pk_as_int=Cast('object_pk', output_field=IntegerField())
        ).filter(
            object_pk_as_int__in=targets_for_user
        ).order_by('-submit_date')[:limit]
    }


@register.filter
def truncate_number(value):
    """
    Truncates a numerical value to four decimal places for display purposes. Etienne Bachelet advised that three
    decimal places was insufficient precision, but that four would be more acceptable.
    """
    try:
        return '%.4f' % value
    except Exception:
        return value
