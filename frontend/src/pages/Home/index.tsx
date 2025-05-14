import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import CreateProductFeature from '../../features/create-product';
import SelectInput from '../../shared/ui/SelectInput';
import Button from '../../shared/ui/Button';
import { SORT_OPTIONS } from '../../entities/product/constants';
import usePollingProducts from '../../entities/product/hooks/usePollingProducts';
import ProductGrid from '../../entities/product/ui/ProductGrid';
import './styles.css';

const Home: React.FC = () => {
  const navigate = useNavigate();
  
  // State for sorting
  const [sortOption, setSortOption] = useState('');
  const [sortedProducts, setSortedProducts] = useState<any[]>([]);
  
  // Use polling for real-time updates
  const { 
    products,
    status,
    error,
    isPolling,
    startPolling,
    stopPolling,
    handleProductCreated,
    refetch
  } = usePollingProducts({
    interval: 10000, // Poll every 10 seconds
    // When we get updated data and sorting is active, we need to apply the sort
    onDataUpdated: (newProducts) => {
      if (sortOption) {
        const selectedOption = SORT_OPTIONS.find(option => option.value === sortOption);
        if (selectedOption) {
          handleSortProducts(newProducts, selectedOption.field, selectedOption.direction === 'asc');
        } else {
          setSortedProducts(newProducts);
        }
      } else {
        setSortedProducts(newProducts);
      }
    }
  });
  
  // Initialize sorted products with the fetched products
  useEffect(() => {
    setSortedProducts(products);
  }, [products]);
  
  // Handle sorting client-side to maintain sort during polling
  const handleSortProducts = (productsToSort: any[], field: string, ascending: boolean) => {
    const sorted = [...productsToSort].sort((a, b) => {
      // Handle string fields
      if (typeof a[field] === 'string') {
        const valueA = a[field].toUpperCase();
        const valueB = b[field].toUpperCase();
        return ascending 
          ? valueA.localeCompare(valueB) 
          : valueB.localeCompare(valueA);
      }
      
      // Handle numeric fields
      return ascending 
        ? a[field] - b[field] 
        : b[field] - a[field];
    });
    
    setSortedProducts(sorted);
  };

  // Apply sorting transformation
  const handleSort = (value: string) => {
    setSortOption(value);
    
    if (!value) {
      setSortedProducts(products);
      return;
    }
    
    const selectedOption = SORT_OPTIONS.find(option => option.value === value);
    
    if (!selectedOption) {
      return;
    }
    
    handleSortProducts(products, selectedOption.field, selectedOption.direction === 'asc');
  };
  
  // Toggle polling
  const togglePolling = () => {
    if (isPolling) {
      stopPolling();
    } else {
      startPolling();
    }
  };

  return (
    <div className="home-page">
      <div className="home-page__header">
        <h1 className="home-page__title">Product Dashboard</h1>
        <div className="home-page__actions">
          <Button 
            onClick={() => navigate('/products')}
            variant="outline"
          >
            Advanced Filters
          </Button>
        </div>
      </div>
      
      <div className="home-page__controls">
        <div className="home-page__sort">
          <SelectInput
            label="Sort by"
            options={SORT_OPTIONS}
            value={sortOption}
            onChange={handleSort}
          />
        </div>
        
        <div className="home-page__polling-controls">
          <Button
            onClick={togglePolling}
            variant={isPolling ? "secondary" : "primary"}
          >
            {isPolling ? "Pause Real-time Updates" : "Enable Real-time Updates"}
          </Button>
          
          <Button
            onClick={refetch}
            variant="outline"
            className="ml-2"
          >
            Refresh Now
          </Button>
        </div>
      </div>
      
      <ProductGrid
        products={sortedProducts}
        loading={status === 'loading'}
        error={error?.message || null}
        onRetry={refetch}
        emptyAction={<CreateProductFeature onProductCreated={handleProductCreated} />}
      />
      
      {isPolling && (
        <div className="home-page__polling-indicator">
          <div className="home-page__polling-dot"></div>
          <span>Real-time updates enabled</span>
        </div>
      )}
    </div>
  );
};

export default Home;
