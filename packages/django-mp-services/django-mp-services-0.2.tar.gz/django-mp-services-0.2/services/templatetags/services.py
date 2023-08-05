
from django import template
from django.apps import apps


register = template.Library()


@register.simple_tag()
def get_service_categories():
    return apps.get_model('services', 'ServiceCategory').objects.all()
