from django.apps import AppConfig


class PatientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patient"
    verbose_name = u"病人管理"
