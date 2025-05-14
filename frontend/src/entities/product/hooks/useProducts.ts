import { useState, useCallback } from 'react';
import { fetchData, FetchOptions } from '../../../shared/lib/api';
import { API_ENDPOINTS } from '../../../shared/config/api';
import { Product } from '../model';
import { clearCachedItem } from '../../../shared/lib/cache';

interface UseProductsState {
  products: Product[];
  loading: boolean;
  error: string | null;
}

interface UseProductsResult extends UseProductsState {
  fetchProducts: (forceRefresh?: boolean) => Promise<void>;
  sortProducts: (field: string, ascending: boolean) => Promise<void>;
  filterProducts: (field: string, operator: string, value: string | number) => Promise<void>;
  resetProducts: () => Promise<void>;
  handleProductCreated: (product: Product) => void;
}

/**
 * Custom hook for managing product data
 * Provides functions for fetching, sorting, and filtering products
 */
export function useProducts(): UseProductsResult {
  const [state, setState] = useState<UseProductsState>({
    products: [],
    loading: false,
    error: null,
  });

  // Generate cache key for products
  const getProductsCacheKey = () => API_ENDPOINTS.PRODUCTS;

  // Fetch all products
  const fetchProducts = useCallback(async (forceRefresh = false) => {
    try {
      setState(prev => ({ ...prev, loading: true }));
      
      // Use cache options
      const options: FetchOptions = {
        forceRefresh,
        cacheTime: 2 // Cache for 2 minutes
      };
      
      const data = await fetchData<{ data: Product[] }>(
        API_ENDPOINTS.PRODUCTS,
        undefined,
        options
      );
      
      setState({
        products: data.data,
        loading: false,
        error: null,
      });
    } catch (err) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: 'Failed to fetch products',
      }));
      console.error(err);
    }
  }, []);

  // Sort products
  const sortProducts = useCallback(async (field: string, ascending: boolean) => {
    try {
      setState(prev => ({ ...prev, loading: true }));
      
      const params = {
        field,
        ascending,
      };
      
      // Don't cache sorted results
      const options: FetchOptions = {
        useCache: false
      };
      
      const data = await fetchData<{ data: Product[] }>(
        `${API_ENDPOINTS.TRANSFORM}sort/`,
        params,
        options
      );
      
      setState(prev => ({
        ...prev,
        products: data.data,
        loading: false,
        error: null,
      }));
    } catch (err) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: 'Failed to sort products',
      }));
      console.error(err);
    }
  }, []);

  // Filter products
  const filterProducts = useCallback(async (field: string, operator: string, value: string | number) => {
    try {
      setState(prev => ({ ...prev, loading: true }));
      
      // Prepare the value for filtering
      let filterValue = value;
      
      // For contains operator with string values, ensure uppercase for case-insensitive search
      if (operator === 'contains' && typeof value === 'string') {
        filterValue = value.toUpperCase();
      }
      
      const params = {
        field,
        operator,
        value: filterValue,
      };
      
      // Don't cache filtered results
      const options: FetchOptions = {
        useCache: false
      };
      
      console.log('Filtering products with params:', params);
      
      const data = await fetchData<{ data: Product[] }>(
        `${API_ENDPOINTS.TRANSFORM}filter/`,
        params,
        options
      );
      
      console.log('Filter response:', data);
      
      if (data.data.length === 0) {
        console.log('No products found matching filter criteria');
      }
      
      setState(prev => ({
        ...prev,
        products: data.data,
        loading: false,
        error: null,
      }));
    } catch (err) {
      console.error('Filter error:', err);
      setState(prev => ({
        ...prev,
        loading: false,
        error: 'Failed to filter products',
      }));
    }
  }, []);

  // Reset products (fetch all again)
  const resetProducts = useCallback(async () => {
    await fetchProducts(true); // Force refresh from API
  }, [fetchProducts]);

  // Handler for when a new product is created
  const handleProductCreated = useCallback((product: Product) => {
    // Invalidate products cache when a new product is created
    clearCachedItem(getProductsCacheKey());
    fetchProducts(true); // Force refresh from API
  }, [fetchProducts]);

  return {
    ...state,
    fetchProducts,
    sortProducts,
    filterProducts,
    resetProducts,
    handleProductCreated,
  };
}

export default useProducts; 