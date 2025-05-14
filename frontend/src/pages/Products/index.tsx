import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useToggle } from '../../shared/hooks/useToggle';
import CreateProductFeature from '../../features/create-product';
import Button from '../../shared/ui/Button';
import Input from '../../shared/ui/Input';
import SelectInput from '../../shared/ui/SelectInput';
import { fetchData } from '../../shared/lib/api';
import { API_ENDPOINTS } from '../../shared/config/api';
import {
  FILTER_OPERATORS, 
  PRODUCT_FIELD_LABELS, 
  AGGREGATE_OPERATIONS
} from '../../entities/product/constants';
import useProducts from '../../entities/product/hooks/useProducts';
import ProductGrid from '../../entities/product/ui/ProductGrid';
import './styles.css';

const Products: React.FC = () => {
  const navigate = useNavigate();
  const { 
    products, 
    loading, 
    error, 
    fetchProducts, 
    filterProducts, 
    handleProductCreated 
  } = useProducts();
  
  const [showFilters, toggleFilters] = useToggle(false);
  
  // Filter state
  const [filterField, setFilterField] = useState('');
  const [filterOperator, setFilterOperator] = useState('');
  const [filterValue, setFilterValue] = useState('');
  
  // Aggregation state
  const [aggregateField, setAggregateField] = useState('');
  const [aggregateOperation, setAggregateOperation] = useState('');
  const [aggregateResult, setAggregateResult] = useState<number | null>(null);
  
  // Fetch products on component mount
  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);
  
  // Apply filter transformation
  const handleFilter = async () => {
    if (!filterField || !filterOperator || !filterValue) {
      return;
    }
    
    // Convert value to the appropriate type based on the field and operator
    let value;
    
    // For 'contains' operator, always use string and convert to uppercase for case-insensitive search
    if (filterOperator === 'contains') {
      if (filterValue.trim() === '') {
        alert('Please enter a search term');
        return;
      }
      value = filterValue.toUpperCase();
    } 
    // For numeric fields, parse as number
    else if (filterField === 'id' || filterField === 'price' || filterField === 'quantity') {
      const parsedValue = parseFloat(filterValue);
      
      // Validate numeric input
      if (isNaN(parsedValue)) {
        alert(`Please enter a valid numeric value for ${filterField}`);
        return;
      }
      
      // Additional validation for specific fields
      if (filterField === 'id' && parsedValue <= 0) {
        alert('ID must be a positive number');
        return;
      }
      
      if ((filterField === 'price' || filterField === 'quantity') && parsedValue < 0) {
        alert(`${filterField} cannot be negative`);
        return;
      }
      
      value = parsedValue;
    } 
    // For other text fields
    else {
      value = filterValue;
    }
    
    try {
      console.log(`Filtering by ${filterField} with params:`, { field: filterField, operator: filterOperator, value });
      await filterProducts(filterField, filterOperator, value);
    } catch (error) {
      console.error(`Error filtering by ${filterField}:`, error);
    }
  };
  
  // Apply aggregation
  const handleAggregate = async () => {
    if (!aggregateField || !aggregateOperation) {
      return;
    }
    
    try {
      const params = {
        field: aggregateField,
        operation: aggregateOperation
      };
      
      // We'll keep this as is since it's specific to this page
      const result = await fetchData<{ result: number }>(
        `${API_ENDPOINTS.TRANSFORM}aggregate/`,
        params
      );
      
      setAggregateResult(result.result);
    } catch (err) {
      console.error('Failed to calculate aggregate', err);
      setAggregateResult(null);
    }
  };
  
  // Reset all filters and aggregations
  const handleReset = () => {
    setFilterField('');
    setFilterOperator('');
    setFilterValue('');
    setAggregateField('');
    setAggregateOperation('');
    setAggregateResult(null);
    fetchProducts();
  };
  
  // Handle field change and reset related inputs
  const handleFieldChange = (value: string) => {
    // If field is changing, reset operator and value
    if (value !== filterField) {
      // Set appropriate default operator based on field type
      if (value === 'name' || value === 'category') {
        // For text fields, default to 'contains'
        setFilterOperator('contains');
      } else if (value === 'id' || value === 'price' || value === 'quantity') {
        // For numeric fields, default to 'eq'
        setFilterOperator('eq');
      } else {
        setFilterOperator('');
      }
      setFilterValue('');
    }
    setFilterField(value);
  };
  
  // Handle aggregate field change and reset related inputs
  const handleAggregateFieldChange = (value: string) => {
    // If field is changing, reset operation
    if (value !== aggregateField) {
      setAggregateOperation('');
      setAggregateResult(null);
    }
    setAggregateField(value);
  };
  
  // Get filtered operator options based on selected field
  const getOperatorOptions = () => {
    // For text fields (name, category), only show 'contains' operator
    if (filterField === 'name' || filterField === 'category') {
      return FILTER_OPERATORS.filter(op => op.value === 'contains');
    }
    
    // For numeric fields (id, price, quantity), exclude 'contains' operator
    if (filterField === 'id' || filterField === 'price' || filterField === 'quantity') {
      return FILTER_OPERATORS.filter(op => op.value !== 'contains');
    }
    
    return FILTER_OPERATORS;
  };
  
  // Generate field options for dropdowns
  const fieldOptions = Object.entries(PRODUCT_FIELD_LABELS)
    .map(([key, label]) => ({
      value: key,
      label
    }));
  
  // Handle value change with validation
  const handleValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    
    // For numeric fields, validate input
    if (filterField === 'id' || filterField === 'price' || filterField === 'quantity') {
      // Allow empty value for clearing the input
      if (newValue === '') {
        setFilterValue('');
        return;
      }
      
      // Check if value is a valid number
      const parsedValue = parseFloat(newValue);
      if (isNaN(parsedValue)) {
        return; // Don't update state if not a valid number
      }
      
      // Additional validation for specific fields
      if (filterField === 'id' && parsedValue <= 0) {
        return; // Don't update if ID is not positive
      }
      
      if ((filterField === 'price' || filterField === 'quantity') && parsedValue < 0) {
        return; // Don't update if price/quantity is negative
      }
    }
    
    setFilterValue(newValue);
  };
  
  return (
    <div className="products-page">
      <div className="products-page__header">
        <h1 className="products-page__title">Products Management</h1>
        <div className="products-page__actions">
          <Button 
            variant="outline"
            onClick={() => navigate('/')}
            className="mr-2"
          >
            Go to Dashboard
          </Button>
          <Button 
            variant="outline"
            onClick={toggleFilters}
            className="mr-2"
          >
            {showFilters ? 'Hide Filters' : 'Show Filters'}
          </Button>
          <CreateProductFeature onProductCreated={handleProductCreated} />
        </div>
      </div>
      
      {showFilters && (
        <div className="products-page__filters">
          <div className="products-page__filter-section">
            <h2 className="products-page__filter-title">Filter Products</h2>
            <div className="products-page__filter-form">
              <SelectInput
                label="Field"
                options={fieldOptions}
                value={filterField}
                onChange={handleFieldChange}
              />
              
              <SelectInput
                label="Operator"
                options={getOperatorOptions()}
                value={filterOperator}
                onChange={setFilterOperator}
                disabled={!filterField}
              />
              
              <Input
                label="Value"
                value={filterValue}
                onChange={handleValueChange}
                type={filterField === 'id' || filterField === 'price' || filterField === 'quantity' ? 'number' : 'text'}
                min={filterField === 'id' ? 1 : filterField === 'price' || filterField === 'quantity' ? 0 : undefined}
                step={filterField === 'price' ? '0.01' : '1'}
                disabled={!filterField}
              />
              
              <Button onClick={handleFilter} disabled={!filterField || !filterOperator || !filterValue}>
                Apply Filter
              </Button>
            </div>
          </div>
          
          <div className="products-page__filter-section">
            <h2 className="products-page__filter-title">Aggregate Data</h2>
            <div className="products-page__filter-form">
              <SelectInput
                label="Field"
                options={fieldOptions.filter(option => 
                  option.value === 'price' || option.value === 'quantity'
                )}
                value={aggregateField}
                onChange={handleAggregateFieldChange}
              />
              
              <SelectInput
                label="Operation"
                options={AGGREGATE_OPERATIONS}
                value={aggregateOperation}
                onChange={setAggregateOperation}
                disabled={!aggregateField}
              />
              
              <Button onClick={handleAggregate} disabled={!aggregateField || !aggregateOperation}>
                Calculate
              </Button>
              
              {aggregateResult !== null && (
                <div className="products-page__aggregate-result">
                  <span className="products-page__aggregate-label">Result:</span>
                  <span className="products-page__aggregate-value">{aggregateResult}</span>
                </div>
              )}
            </div>
          </div>
          
          <Button variant="outline" onClick={handleReset}>
            Reset All
          </Button>
        </div>
      )}
      
      <ProductGrid
        products={products}
        loading={loading}
        error={error}
        onRetry={fetchProducts}
        emptyAction={<CreateProductFeature onProductCreated={handleProductCreated} />}
      />
    </div>
  );
};

export default Products;
