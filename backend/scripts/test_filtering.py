#!/usr/bin/env python
"""
Test script for filter functionality, specifically for ID, Price, and Quantity fields.
This helps diagnose and verify fixes for filtering issues.
"""

import sys
import os
import json
import requests

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

API_BASE_URL = "http://localhost:8000/api/data"

def test_filter_id():
    """Test filtering by ID field with different operators"""
    operators = ["eq", "neq", "gt", "lt"]
    values = [1, 5, 10]
    
    print("\n=== Testing ID Filtering ===")
    for operator in operators:
        for value in values:
            url = f"{API_BASE_URL}/transform/filter/?field=id&operator={operator}&value={value}"
            print(f"\nTesting: {url}")
            try:
                response = requests.get(url)
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    item_count = len(result.get("data", []))
                    print(f"Found {item_count} items")
                else:
                    print(f"Error: {response.text}")
            except Exception as e:
                print(f"Request failed: {str(e)}")

def test_filter_price():
    """Test filtering by price field with different operators"""
    operators = ["eq", "neq", "gt", "lt"]
    values = [10.99, 25.50, 50.00]
    
    print("\n=== Testing Price Filtering ===")
    for operator in operators:
        for value in values:
            url = f"{API_BASE_URL}/transform/filter/?field=price&operator={operator}&value={value}"
            print(f"\nTesting: {url}")
            try:
                response = requests.get(url)
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    item_count = len(result.get("data", []))
                    print(f"Found {item_count} items")
                else:
                    print(f"Error: {response.text}")
            except Exception as e:
                print(f"Request failed: {str(e)}")

def test_filter_quantity():
    """Test filtering by quantity field with different operators"""
    operators = ["eq", "neq", "gt", "lt"]
    values = [5, 10, 20]
    
    print("\n=== Testing Quantity Filtering ===")
    for operator in operators:
        for value in values:
            url = f"{API_BASE_URL}/transform/filter/?field=quantity&operator={operator}&value={value}"
            print(f"\nTesting: {url}")
            try:
                response = requests.get(url)
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    item_count = len(result.get("data", []))
                    print(f"Found {item_count} items")
                else:
                    print(f"Error: {response.text}")
            except Exception as e:
                print(f"Request failed: {str(e)}")

def test_invalid_values():
    """Test filtering with invalid values to ensure proper error handling"""
    test_cases = [
        {"field": "id", "operator": "eq", "value": "abc"},
        {"field": "price", "operator": "gt", "value": "not-a-price"},
        {"field": "quantity", "operator": "lt", "value": "invalid"}
    ]
    
    print("\n=== Testing Invalid Values ===")
    for case in test_cases:
        url = f"{API_BASE_URL}/transform/filter/?field={case['field']}&operator={case['operator']}&value={case['value']}"
        print(f"\nTesting: {url}")
        try:
            response = requests.get(url)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Request failed: {str(e)}")


if __name__ == "__main__":
    print("\n===== Testing Filtering Functionality =====\n")
    
    # Test all filtering functions
    test_filter_id()
    test_filter_price()
    test_filter_quantity()
    test_invalid_values()
    
    print("\n===== Testing Complete =====\n") 