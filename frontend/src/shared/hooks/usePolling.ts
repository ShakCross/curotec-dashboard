import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Options for polling
 */
export interface PollingOptions {
  /** Polling interval in milliseconds (default: 10000) */
  interval?: number;
  /** Whether polling should start immediately (default: true) */
  autoStart?: boolean;
  /** Whether to run the first fetch immediately (default: true) */
  runImmediately?: boolean;
  /** Whether polling is enabled (default: true) */
  enabled?: boolean;
}

/**
 * Custom hook for polling data at regular intervals
 * @param fetchFn - The fetch function to call
 * @param options - Polling options
 * @returns Object with data, status, error, start polling, stop polling, and manual refetch
 */
export function usePolling<T>(
  fetchFn: () => Promise<T>,
  options?: PollingOptions
) {
  const defaultOptions: PollingOptions = {
    interval: 10000, // 10 seconds by default
    autoStart: true,
    runImmediately: true,
    enabled: true,
  };
  
  const pollingOptions = { ...defaultOptions, ...options };
  const { interval, autoStart, runImmediately, enabled } = pollingOptions;
  
  const [data, setData] = useState<T | null>(null);
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [error, setError] = useState<Error | null>(null);
  const [isPolling, setIsPolling] = useState(autoStart && enabled);
  
  // Use a ref for the polling interval to avoid unnecessary re-renders
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  
  // Store the latest fetch function in a ref to avoid dependency issues
  const fetchFnRef = useRef(fetchFn);
  useEffect(() => {
    fetchFnRef.current = fetchFn;
  }, [fetchFn]);
  
  // Function to fetch data
  const fetchData = useCallback(async () => {
    setStatus('loading');
    
    try {
      const result = await fetchFnRef.current();
      setData(result);
      setStatus('success');
      setError(null);
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err : new Error('An error occurred'));
      console.error('Polling error:', err);
    }
  }, []);
  
  // Start polling
  const startPolling = useCallback(() => {
    if (!enabled) return;
    
    setIsPolling(true);
  }, [enabled]);
  
  // Stop polling
  const stopPolling = useCallback(() => {
    setIsPolling(false);
  }, []);
  
  // Clear the interval when component unmounts or when polling stops
  const clearPollingInterval = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);
  
  // Set up and clean up the polling interval
  useEffect(() => {
    // Don't set up polling if it's disabled or not active
    if (!enabled || !isPolling) {
      clearPollingInterval();
      return;
    }
    
    // Run immediately if specified
    if (runImmediately) {
      fetchData();
    }
    
    // Set up the polling interval
    intervalRef.current = setInterval(fetchData, interval);
    
    // Clean up on unmount or when dependencies change
    return () => {
      clearPollingInterval();
    };
  }, [isPolling, interval, enabled, runImmediately, fetchData, clearPollingInterval]);
  
  // Clean up on unmount
  useEffect(() => {
    return () => {
      clearPollingInterval();
    };
  }, [clearPollingInterval]);
  
  return {
    data,
    status,
    error,
    isPolling,
    startPolling,
    stopPolling,
    refetch: fetchData
  };
}

export default usePolling; 