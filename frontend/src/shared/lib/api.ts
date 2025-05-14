import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { API_BASE_URL } from '../config/api';
import { getCachedItem, setCachedItem } from './cache';

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Centralized error handling
    const message = error.response?.data?.error || 'An unexpected error occurred';
    console.error('API Error:', message);
    return Promise.reject(error);
  }
);

/**
 * Options for fetch requests
 */
export interface FetchOptions {
  /** Whether to use cache (default: true) */
  useCache?: boolean;
  /** Cache expiration time in minutes (default: 5) */
  cacheTime?: number;
  /** Force refresh cache even if not expired */
  forceRefresh?: boolean;
}

// Default fetch options
const defaultFetchOptions: FetchOptions = {
  useCache: true,
  cacheTime: 5,
  forceRefresh: false,
};

// Generate a cache key from URL and params
const generateCacheKey = (url: string, params?: Record<string, any>): string => {
  return params ? `${url}:${JSON.stringify(params)}` : url;
};

// Generic typed API functions
export const fetchData = async <T>(
  url: string, 
  params?: Record<string, any>, 
  options?: FetchOptions
): Promise<T> => {
  // Merge default options with provided options
  const fetchOptions: FetchOptions = { ...defaultFetchOptions, ...options };
  const { useCache, cacheTime, forceRefresh } = fetchOptions;
  
  // Create cache key from URL and params
  const cacheKey = generateCacheKey(url, params);
  
  // Try to get from cache if caching is enabled and not forcing refresh
  if (useCache && !forceRefresh) {
    const cachedData = getCachedItem<T>(cacheKey, cacheTime);
    if (cachedData) {
      console.log('Retrieved from cache:', url);
      return cachedData;
    }
  }
  
  // Prepare request config
  const config: AxiosRequestConfig = {};
  if (params) {
    // Ensure numeric values are properly formatted for the API
    const formattedParams: Record<string, any> = {};
    
    Object.entries(params).forEach(([key, value]) => {
      // Keep numbers as numbers, not as strings
      formattedParams[key] = value;
    });
    
    config.params = formattedParams;
    console.log('API Request URL:', url);
    console.log('API Request Params:', formattedParams);
  }
  
  try {
    const response: AxiosResponse<T> = await apiClient.get(url, config);
    console.log('API Response:', response.data);
    
    // Store in cache if caching is enabled
    if (useCache) {
      setCachedItem(cacheKey, response.data);
    }
    
    return response.data;
  } catch (error: any) {
    console.log('API Error Response:', error.response?.data);
    throw error;
  }
};

export const postData = async <T, D>(url: string, data: D): Promise<T> => {
  const response: AxiosResponse<T> = await apiClient.post(url, data);
  return response.data;
};

export const transformData = async <T>(
  transformationType: string, 
  params: Record<string, any>,
  options?: FetchOptions
): Promise<T> => {
  const url = `/data/transform/${transformationType}/`;
  return fetchData<T>(url, params, options);
};

export default apiClient; 