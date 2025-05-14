import { Product } from './model';

/**
 * Product utility functions
 */

// Format price with currency symbol
export const formatPrice = (price: number | null | undefined): string => {
  // Handle invalid values (null, undefined, NaN)
  if (price === null || price === undefined || isNaN(price)) {
    return '$0.00';
  }
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(price);
};

// Format number with thousands separators
export const formatNumber = (num: number | null | undefined): string => {
  // Handle invalid values (null, undefined, NaN)
  if (num === null || num === undefined || isNaN(num)) {
    return '0';
  }
  
  return new Intl.NumberFormat('en-US').format(num);
};

// Calculate total value of a product (price * quantity)
export const calculateProductValue = (product: Product): number => {
  const price = product.price || 0;
  const quantity = product.quantity || 0;
  return price * quantity;
};

// Group products by category
export const groupByCategory = (products: Product[]): Record<string, Product[]> => {
  return products.reduce<Record<string, Product[]>>((acc, product) => {
    const category = product.category;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(product);
    return acc;
  }, {});
};

// Get total inventory value
export const getTotalInventoryValue = (products: Product[]): number => {
  return products.reduce((total, product) => {
    return total + calculateProductValue(product);
  }, 0);
};

// Get total products count
export const getTotalProductsCount = (products: Product[]): number => {
  return products.reduce((total, product) => {
    return total + (product.quantity || 0);
  }, 0);
};

// Get product categories from products
export const getUniqueCategories = (products: Product[]): string[] => {
  const categories = new Set<string>();
  products.forEach(product => categories.add(product.category));
  return Array.from(categories);
}; 