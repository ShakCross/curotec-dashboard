import { useState, useEffect, useCallback } from 'react';
import { ApiStatus } from '../types/common';

interface UseFetchState<T> {
  data: T | null;
  status: ApiStatus;
  error: Error | null;
}

interface UseFetchResult<T> extends UseFetchState<T> {
  refetch: () => Promise<void>;
}

/**
 * Custom hook for fetching data from an API
 * @param fetchFn - The fetch function to call
 * @param dependencies - Dependencies array for when to re-fetch data
 * @param initialFetch - Whether to fetch on mount
 */
export function useFetch<T>(
  fetchFn: () => Promise<T>,
  dependencies: any[] = [],
  initialFetch: boolean = true
): UseFetchResult<T> {
  const [state, setState] = useState<UseFetchState<T>>({
    data: null,
    status: 'idle',
    error: null,
  });

  const fetchData = useCallback(async () => {
    setState(prev => ({ ...prev, status: 'loading' }));
    
    try {
      const data = await fetchFn();
      setState({ data, status: 'success', error: null });
    } catch (error) {
      setState({ data: null, status: 'error', error: error as Error });
    }
  }, [fetchFn]);

  useEffect(() => {
    if (initialFetch) {
      fetchData();
    }
  }, [...dependencies, fetchData, initialFetch]);

  return { ...state, refetch: fetchData };
}

export default useFetch; 