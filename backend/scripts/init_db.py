#!/usr/bin/env python
"""
Script to initialize database tables using SQLAlchemy
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add the data_processing_api directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_processing_api"))

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_processing_api.settings")
django.setup()

from sqlalchemy import create_engine
from django.conf import settings
from shared.db.base_model import Base
from apps.data_processor.infrastructure.models import DataEntry

def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    
    # Create SQLAlchemy engine
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db() 