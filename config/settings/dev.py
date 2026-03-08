from .base import *  # noqa: F401, F403

DEBUG = True

# In dev, show emails in the console instead of sending them
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
