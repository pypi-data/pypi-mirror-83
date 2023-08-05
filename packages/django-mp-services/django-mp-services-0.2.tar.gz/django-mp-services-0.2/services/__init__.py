
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ServicesConfig(AppConfig):
    name = 'services'
    verbose_name = _("Services")


default_app_config = 'services.ServicesConfig'
