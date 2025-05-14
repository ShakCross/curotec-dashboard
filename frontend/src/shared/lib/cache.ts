/**
 * Simple cache utility for storing and retrieving data from localStorage
 * with expiration time support
 */

interface CacheItem<T> {
  data: T;
  timestamp: number;
}

/**
 * Get an item from cache
 * @param key - Cache key
 * @param expirationMinutes - Expiration time in minutes (default: 5)
 * @returns The cached data or null if not found or expired
 */
export function getCachedItem<T>(key: string, expirationMinutes: number = 5): T | null {
  try {
    const cacheKey = `cache_${key}`;
    const cachedData = localStorage.getItem(cacheKey);
    
    if (!cachedData) {
      return null;
    }
    
    const { data, timestamp }: CacheItem<T> = JSON.parse(cachedData);
    const isExpired = Date.now() - timestamp > expirationMinutes * 60 * 1000;
    
    if (isExpired) {
      // Clean up expired items
      localStorage.removeItem(cacheKey);
      return null;
    }
    
    return data;
  } catch (error) {
    console.warn('Error retrieving data from cache:', error);
    return null;
  }
}

/**
 * Store an item in cache
 * @param key - Cache key
 * @param data - Data to cache
 */
export function setCachedItem<T>(key: string, data: T): void {
  try {
    const cacheKey = `cache_${key}`;
    const cacheItem: CacheItem<T> = {
      data,
      timestamp: Date.now(),
    };
    
    localStorage.setItem(cacheKey, JSON.stringify(cacheItem));
  } catch (error) {
    console.warn('Error storing data in cache:', error);
  }
}

/**
 * Clear a specific item from cache
 * @param key - Cache key
 */
export function clearCachedItem(key: string): void {
  try {
    const cacheKey = `cache_${key}`;
    localStorage.removeItem(cacheKey);
  } catch (error) {
    console.warn('Error clearing cached item:', error);
  }
}

/**
 * Clear all cached items
 */
export function clearCache(): void {
  try {
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('cache_')) {
        localStorage.removeItem(key);
      }
    });
  } catch (error) {
    console.warn('Error clearing cache:', error);
  }
} 