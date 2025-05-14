import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestDataProcessorViews:
    """Test cases for data processor views"""
    
    @pytest.fixture
    def api_client(self):
        """Create API client"""
        return APIClient()
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return [
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
            }
        ]
    
    def test_process_data(self, api_client, sample_data):
        """Test processing data"""
        url = reverse('process_data')
        response = api_client.post(url, sample_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == len(sample_data)
        
        for item in response.data:
            assert 'id' in item
            assert 'name' in item
            assert 'price' in item
            assert 'quantity' in item
            assert 'category' in item
    
    def test_filter_data(self, api_client, sample_data):
        """Test filtering data"""
        # First process the data
        process_url = reverse('process_data')
        api_client.post(process_url, sample_data, format='json')
        
        # Then filter it
        url = reverse('transform_data', kwargs={'transformation_type': 'filter'})
        response = api_client.get(f"{url}?field=category&value=Electronics")
        
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert len(response.data['data']) == 2  # Two items have category 'Electronics'
        
        for item in response.data['data']:
            assert item['category'] == 'Electronics'
    
    def test_sort_data(self, api_client, sample_data):
        """Test sorting data"""
        # First process the data
        process_url = reverse('process_data')
        api_client.post(process_url, sample_data, format='json')
        
        # Then sort it
        url = reverse('transform_data', kwargs={'transformation_type': 'sort'})
        response = api_client.get(f"{url}?field=price&ascending=true")
        
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert len(response.data['data']) == 3
        
        # Check if sorted in ascending order
        prices = [item['price'] for item in response.data['data']]
        assert prices == sorted(prices)
    
    def test_aggregate_data(self, api_client, sample_data):
        """Test aggregating data"""
        # First process the data
        process_url = reverse('process_data')
        api_client.post(process_url, sample_data, format='json')
        
        # Then aggregate it
        url = reverse('transform_data', kwargs={'transformation_type': 'aggregate'})
        response = api_client.get(f"{url}?field=price&operation=sum")
        
        assert response.status_code == status.HTTP_200_OK
        assert 'result' in response.data
        
        # Sum of all prices should be 25.99 + 15.50 + 99.99 = 141.48
        expected_sum = sum(item['price'] for item in sample_data)
        assert response.data['result'] == pytest.approx(expected_sum)
    
    def test_filter_data_by_id(self, api_client, sample_data):
        """Test filtering data by ID"""
        # First process the data
        process_url = reverse('process_data')
        response = api_client.post(process_url, sample_data, format='json')
        
        # Get the ID of the first created item
        first_item_id = response.data[0]['id']
        
        # Then filter by that ID
        url = reverse('transform_data', kwargs={'transformation_type': 'filter'})
        response = api_client.get(f"{url}?field=id&value={first_item_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert len(response.data['data']) == 1  # Should find exactly one item
        assert response.data['data'][0]['id'] == first_item_id 