"""
WSGI config for data_processing_api project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_processing_api.settings')

application = get_wsgi_application() 