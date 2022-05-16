from django.apps import AppConfig

"""
here we difine the application that we have added to settings.py. This will tell our website to look for the polling application
"""
class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
