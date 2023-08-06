from django.apps import AppConfig


class SoloAppConfig(AppConfig):
    name = 'box.core.sw_solo'
    verbose_name = "solo"
    verbose_name_plural = "solo"

default_app_config = 'box.core.sw_solo.SoloAppConfig'

