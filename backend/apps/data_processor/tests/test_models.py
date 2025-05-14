import pytest
from apps.data_processor.domain.models import DataItem, DataSet, TransformationType

class TestDataItem:
    """Test cases for DataItem domain model"""
    
    def test_init_with_defaults(self):
        """Test initialization with default values"""
        item = DataItem()
        assert item.id is None
        assert item.numeric_fields == {}
        assert item.string_fields == {}
    
    def test_init_with_values(self):
        """Test initialization with provided values"""
        item = DataItem(
            id=1,
            numeric_fields={"price": 10.99, "quantity": 5},
            string_fields={"name": "Test Product", "category": "Test"}
        )
        assert item.id == 1
        assert item.numeric_fields == {"price": 10.99, "quantity": 5}
        assert item.string_fields == {"name": "Test Product", "category": "Test"}
    
    def test_to_dict(self):
        """Test converting to dictionary"""
        item = DataItem(
            id=1,
            numeric_fields={"price": 10.99, "quantity": 5},
            string_fields={"name": "Test Product", "category": "Test"}
        )
        result = item.to_dict()
        expected = {
            "id": 1,
            "price": 10.99,
            "quantity": 5,
            "name": "Test Product",
            "category": "Test"
        }
        assert result == expected
    
    def test_to_dict_without_id(self):
        """Test converting to dictionary without ID"""
        item = DataItem(
            numeric_fields={"price": 10.99},
            string_fields={"name": "Test Product"}
        )
        result = item.to_dict()
        expected = {
            "price": 10.99,
            "name": "Test Product"
        }
        assert result == expected
    
    def test_field_overriding(self):
        """Test that string fields override numeric fields with the same name"""
        item = DataItem(
            numeric_fields={"price": 10.99, "ambiguous": 123},
            string_fields={"name": "Test Product", "ambiguous": "string value"}
        )
        result = item.to_dict()
        # The string field should override the numeric field
        assert result["ambiguous"] == "string value"


class TestDataSet:
    """Test cases for DataSet domain model"""
    
    @pytest.fixture
    def sample_items(self):
        """Create a sample dataset for testing"""
        return [
            DataItem(
                id=1,
                numeric_fields={"price": 10.99, "quantity": 5},
                string_fields={"name": "Product A", "category": "Electronics"}
            ),
            DataItem(
                id=2,
                numeric_fields={"price": 5.99, "quantity": 10},
                string_fields={"name": "Product B", "category": "Books"}
            ),
            DataItem(
                id=3,
                numeric_fields={"price": 15.99, "quantity": 2},
                string_fields={"name": "Product C", "category": "Electronics"}
            ),
            DataItem(
                id=4,
                numeric_fields={"price": 0, "quantity": 0},
                string_fields={"name": "Free Product", "category": "Digital"}
            ),
            DataItem(
                id=5,
                # Missing price field
                numeric_fields={"quantity": 1},
                string_fields={"name": "Incomplete Product", "category": "Other"}
            ),
            DataItem(
                # No ID
                numeric_fields={"price": 100, "quantity": 1},
                string_fields={"name": "No ID Product", "category": "Other"}
            )
        ]
    
    @pytest.fixture
    def dataset(self, sample_items):
        """Create a dataset from sample items"""
        return DataSet(items=sample_items)
    
    def test_filter_by_id(self, dataset):
        """Test filtering by ID"""
        # Filter by existing ID
        result = dataset.filter("id", 3)
        assert len(result.items) == 1
        assert result.items[0].id == 3
        
        # Filter by non-existent ID
        result = dataset.filter("id", 999)
        assert len(result.items) == 0
        
        # Filter items without ID
        result = dataset.filter("id", None)
        assert len(result.items) == 0
    
    def test_filter_by_numeric_field(self, dataset):
        """Test filtering by numeric field"""
        # Equal operator
        result = dataset.filter("price", 10.99)
        assert len(result.items) == 1
        assert result.items[0].id == 1
        
        # Not equal operator
        result = dataset.filter("price", 10.99, "neq")
        assert len(result.items) == 4  # Excludes item with price=10.99 and item with missing price
        
        # Greater than operator
        result = dataset.filter("price", 10, "gt")
        assert len(result.items) == 3
        # Items with ID 1, 3 and the one without ID have price > 10
        assert 1 in [item.id for item in result.items if item.id is not None]
        assert 3 in [item.id for item in result.items if item.id is not None]
        
        # Less than operator
        result = dataset.filter("price", 10, "lt")
        assert len(result.items) == 2
        assert {item.id for item in result.items} == {2, 4}
        
        # Filter by non-existent field
        result = dataset.filter("non_existent", 10)
        assert len(result.items) == 0
        
        # Filter by field with zero value
        result = dataset.filter("price", 0)
        assert len(result.items) == 1
        assert result.items[0].id == 4
    
    def test_filter_by_string_field(self, dataset):
        """Test filtering by string field"""
        # Equal operator
        result = dataset.filter("category", "Electronics")
        assert len(result.items) == 2
        assert {item.id for item in result.items} == {1, 3}
        
        # Not equal operator
        result = dataset.filter("category", "Electronics", "neq")
        assert len(result.items) == 4
        
        # Contains operator
        result = dataset.filter("name", "Product", "contains")
        assert len(result.items) == 6  # All items contain "Product" in name
        
        # Contains operator with case insensitivity
        result = dataset.filter("name", "product", "contains")
        assert len(result.items) == 6  # Case-insensitive search
        
        # Contains operator with partial match
        result = dataset.filter("name", "Free", "contains")
        assert len(result.items) == 1
        assert result.items[0].id == 4
    
    def test_filter_with_invalid_operator(self, dataset):
        """Test filtering with invalid operator"""
        # Invalid operator should return empty result
        result = dataset.filter("price", 10, "invalid_op")
        assert len(result.items) == 0
    
    def test_filter_empty_dataset(self):
        """Test filtering an empty dataset"""
        empty_dataset = DataSet(items=[])
        result = empty_dataset.filter("price", 10)
        assert len(result.items) == 0
    
    def test_sort_by_id(self, dataset):
        """Test sorting by ID"""
        # Ascending sort
        result = dataset.sort("id")
        assert [item.id for item in result.items if item.id is not None] == [1, 2, 3, 4, 5]
        
        # Descending sort
        result = dataset.sort("id", ascending=False)
        assert [item.id for item in result.items if item.id is not None] == [5, 4, 3, 2, 1]
    
    def test_sort_by_numeric_field(self, dataset):
        """Test sorting by numeric field"""
        # Ascending sort by price
        result = dataset.sort("price")
        prices = [item.numeric_fields.get("price") for item in result.items if "price" in item.numeric_fields]
        assert prices == [0, 5.99, 10.99, 15.99, 100]
        
        # Descending sort by price
        result = dataset.sort("price", ascending=False)
        prices = [item.numeric_fields.get("price") for item in result.items if "price" in item.numeric_fields]
        assert prices == [100, 15.99, 10.99, 5.99, 0]
        
        # Sort by quantity
        result = dataset.sort("quantity")
        quantities = [item.numeric_fields.get("quantity") for item in result.items]
        assert quantities == [0, 1, 1, 2, 5, 10]
    
    def test_sort_by_string_field(self, dataset):
        """Test sorting by string field"""
        # Ascending sort by name
        result = dataset.sort("name")
        names = [item.string_fields.get("name") for item in result.items]
        assert names == ["Free Product", "Incomplete Product", "No ID Product", "Product A", "Product B", "Product C"]
        
        # Descending sort by category
        result = dataset.sort("category", ascending=False)
        categories = [item.string_fields.get("category") for item in result.items]
        # Categories in descending order: Other, Other, Electronics, Electronics, Digital, Books
        assert categories[0] == "Other"
        assert categories[-1] == "Books"
    
    def test_sort_by_non_existent_field(self, dataset):
        """Test sorting by non-existent field"""
        result = dataset.sort("non_existent")
        # Should return empty dataset since no items have this field
        assert len(result.items) == 0
    
    def test_sort_empty_dataset(self):
        """Test sorting an empty dataset"""
        empty_dataset = DataSet(items=[])
        result = empty_dataset.sort("price")
        assert len(result.items) == 0
    
    def test_sort_with_missing_fields(self, dataset):
        """Test sorting with some items missing the sort field"""
        # Sort by price (one item is missing price)
        result = dataset.sort("price")
        # Should only include items with the price field
        assert len(result.items) == 5
        # Item with ID 5 should be excluded (no price field)
        assert 5 not in [item.id for item in result.items if item.id is not None]
    
    def test_aggregate_sum(self, dataset):
        """Test sum aggregation"""
        result = dataset.aggregate("price", "sum")
        # Sum of all prices: 10.99 + 5.99 + 15.99 + 0 + 100 = 132.97
        assert result["result"] == pytest.approx(132.97)
        
        # Aggregate field that some items don't have
        result = dataset.aggregate("missing_field", "sum")
        assert result["result"] is None
    
    def test_aggregate_avg(self, dataset):
        """Test average aggregation"""
        result = dataset.aggregate("price", "avg")
        # Average of prices: (10.99 + 5.99 + 15.99 + 0 + 100) / 5 = 26.594
        assert result["result"] == pytest.approx(26.594)
    
    def test_aggregate_min(self, dataset):
        """Test minimum aggregation"""
        result = dataset.aggregate("price", "min")
        assert result["result"] == 0
        
        result = dataset.aggregate("quantity", "min")
        assert result["result"] == 0
    
    def test_aggregate_max(self, dataset):
        """Test maximum aggregation"""
        result = dataset.aggregate("price", "max")
        assert result["result"] == 100
        
        result = dataset.aggregate("quantity", "max")
        assert result["result"] == 10
    
    def test_aggregate_count(self, dataset):
        """Test count aggregation"""
        result = dataset.aggregate("price", "count")
        # Count of items with price field
        assert result["result"] == 5
        
        result = dataset.aggregate("quantity", "count")
        # All items have quantity field
        assert result["result"] == 6
    
    def test_aggregate_invalid_operation(self, dataset):
        """Test aggregation with invalid operation"""
        result = dataset.aggregate("price", "invalid_op")
        assert result["result"] is None
    
    def test_aggregate_non_numeric_field(self, dataset):
        """Test aggregation on non-numeric field"""
        result = dataset.aggregate("name", "sum")
        # Should return None as name is not a numeric field
        assert result["result"] is None
    
    def test_aggregate_empty_dataset(self):
        """Test aggregation on empty dataset"""
        empty_dataset = DataSet(items=[])
        result = empty_dataset.aggregate("price", "sum")
        assert result["result"] is None
    
    def test_to_dict(self, dataset):
        """Test converting dataset to list of dictionaries"""
        result = dataset.to_dict()
        assert len(result) == 6
        # Check first item
        assert result[0]["id"] == 1
        assert result[0]["price"] == 10.99
        assert result[0]["name"] == "Product A"


class TestTransformationType:
    """Test cases for TransformationType enum"""
    
    def test_has_value(self):
        """Test has_value method"""
        assert TransformationType.has_value("filter") is True
        assert TransformationType.has_value("sort") is True
        assert TransformationType.has_value("aggregate") is True
        assert TransformationType.has_value("invalid") is False
        assert TransformationType.has_value("") is False
        assert TransformationType.has_value(None) is False 