#!/usr/bin/env python
"""
Script to load test data into the database
"""

import os
import sys
import django
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add the data_processing_api directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_processing_api"))

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_processing_api.settings")
django.setup()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.conf import settings
from apps.data_processor.infrastructure.models import DataEntry
from apps.data_processor.domain.models import DataItem

# Test data
TEST_DATA = [
    {
        "name": "Product A",
        "price": 25.99,
        "quantity": 10,
        "category": "Electronics"
    },
    {
        "name": "Product B",
        "price": 15.50,
        "quantity": 5,
        "category": "Books"
    },
    {
        "name": "Product C",
        "price": 99.99,
        "quantity": 2,
        "category": "Electronics"
    },
    {
        "name": "Product D",
        "price": 32.75,
        "quantity": 8,
        "category": "Clothing"
    },
    {
        "name": "Product E",
        "price": 149.99,
        "quantity": 1,
        "category": "Electronics"
    }
]

def load_test_data():
    """Load test data into the database"""
    print("Loading test data...")
    
    # Create SQLAlchemy engine and session
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Convert test data to DataEntry objects
        entries = []
        for item_data in TEST_DATA:
            numeric_fields = {}
            string_fields = {}
            
            # Separate numeric and string fields
            for key, value in item_data.items():
                if isinstance(value, (int, float)):
                    numeric_fields[key] = value
                elif isinstance(value, str):
                    string_fields[key] = value
            
            # Create DataItem domain model
            data_item = DataItem(
                numeric_fields=numeric_fields,
                string_fields=string_fields
            )
            
            # Convert to DataEntry infrastructure model
            entry = DataEntry.from_domain(data_item)
            entries.append(entry)
        
        # Add all entries to the session
        session.add_all(entries)
        session.commit()
        
        # Print the number of entries created
        print(f"Successfully loaded {len(entries)} test data entries.")
        
        # Query and print the entries for verification
        all_entries = session.query(DataEntry).all()
        for entry in all_entries:
            domain_item = entry.to_domain()
            print(f"ID: {domain_item.id}, Data: {json.dumps(domain_item.to_dict())}")
        
    except Exception as e:
        session.rollback()
        print(f"Error loading test data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    load_test_data() 