/**
 * Product constants 
 */

// Product field labels
export const PRODUCT_FIELD_LABELS = {
  id: 'ID',
  name: 'Product Name',
  price: 'Price',
  quantity: 'Quantity',
  category: 'Category',
};

// Product categories
export const PRODUCT_CATEGORIES = [
  'Electronics',
  'Books',
  'Clothing',
  'Office Supplies',
  'Household',
  'Food & Beverage',
  'Sports & Outdoors',
  'Health & Beauty',
  'Toys & Games',
  'Automotive',
  'Other',
];

// Product field types for form handling
export const PRODUCT_FIELD_TYPES: Record<string, 'text' | 'number' | 'select'> = {
  name: 'text',
  price: 'number',
  quantity: 'number',
  category: 'select',
};

// Sorting options
export const SORT_OPTIONS = [
  { value: 'price_asc', label: 'Price (Low to High)', field: 'price', direction: 'asc' as const },
  { value: 'price_desc', label: 'Price (High to Low)', field: 'price', direction: 'desc' as const },
  { value: 'name_asc', label: 'Name (A-Z)', field: 'name', direction: 'asc' as const },
  { value: 'name_desc', label: 'Name (Z-A)', field: 'name', direction: 'desc' as const },
  { value: 'quantity_asc', label: 'Quantity (Low to High)', field: 'quantity', direction: 'asc' as const },
  { value: 'quantity_desc', label: 'Quantity (High to Low)', field: 'quantity', direction: 'desc' as const },
];

// Filter operators
export const FILTER_OPERATORS = [
  { value: 'eq', label: 'Equals' },
  { value: 'neq', label: 'Not Equals' },
  { value: 'gt', label: 'Greater Than' },
  { value: 'lt', label: 'Less Than' },
  { value: 'contains', label: 'Contains' },
];

// Aggregate operations
export const AGGREGATE_OPERATIONS = [
  { value: 'sum', label: 'Sum' },
  { value: 'avg', label: 'Average' },
  { value: 'min', label: 'Minimum' },
  { value: 'max', label: 'Maximum' },
  { value: 'count', label: 'Count' },
]; 