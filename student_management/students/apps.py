from django.apps import AppConfig


class StudentsConfig(AppConfig):
    """
    Configuration for the students app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'

    def ready(self):
        import students.signals  # Import signals to ensure they are registered