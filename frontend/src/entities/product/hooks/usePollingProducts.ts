import { useCallback } from 'react';
import { usePolling, PollingOptions } from '../../../shared/hooks/usePolling';
import { fetchData } from '../../../shared/lib/api';
import { API_ENDPOINTS } from '../../../shared/config/api';
import { Product } from '../model';
import { clearCachedItem } from '../../../shared/lib/cache';

interface ProductsResponse {
  data: Product[];
}

interface UsePollingProductsOptions extends PollingOptions {
  onDataUpdated?: (products: Product[]) => void;
}

/**
 * Custom hook for polling products data at regular intervals
 */
export function usePollingProducts(options?: UsePollingProductsOptions) {
  // Generate cache key for products
  const getProductsCacheKey = () => API_ENDPOINTS.PRODUCTS;
  
  // Create a fetch function that will be called by the polling hook
  const fetchProducts = useCallback(async () => {
    // Always force refresh when polling to get the latest data
    const response = await fetchData<ProductsResponse>(
      API_ENDPOINTS.PRODUCTS,
      undefined,
      { forceRefresh: true }
    );
    
    // Call the onDataUpdated callback if provided
    if (options?.onDataUpdated) {
      options.onDataUpdated(response.data);
    }
    
    return response;
  }, [options]);
  
  // Use the polling hook with our fetch function
  const polling = usePolling<ProductsResponse>(fetchProducts, {
    interval: options?.interval || 5000, // Poll every 5 seconds by default
    ...options
  });
  
  // Handler for when a new product is created
  const handleProductCreated = useCallback((product: Product) => {
    // Invalidate products cache when a new product is created
    clearCachedItem(getProductsCacheKey());
    
    // Trigger an immediate refresh
    polling.refetch();
  }, [polling]);
  
  return {
    ...polling,
    products: polling.data?.data || [],
    handleProductCreated
  };
}

export default usePollingProducts; 