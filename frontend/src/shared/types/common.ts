/**
 * Common types used across the application
 */

// API response status
export type ApiStatus = 'idle' | 'loading' | 'success' | 'error';

// Pagination type
export interface Pagination {
  page: number;
  pageSize: number;
  total: number;
}

// Sort direction
export type SortDirection = 'asc' | 'desc';

// Sort option
export interface SortOption {
  field: string;
  direction: SortDirection;
}

// Filter operator
export type FilterOperator = 'eq' | 'neq' | 'gt' | 'lt' | 'contains';

// Filter option
export interface FilterOption {
  field: string;
  value: string | number;
  operator: FilterOperator;
}

// Transformation parameters
export interface TransformParams {
  filter?: FilterOption;
  sort?: SortOption;
  aggregate?: {
    field: string;
    operation: string;
  };
} 