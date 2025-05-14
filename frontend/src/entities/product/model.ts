/**
 * Product domain entity models
 */

// Basic product interface
export interface Product {
  id: number;
  name: string;
  price: number;
  quantity: number;
  category: string;
  [key: string]: string | number; // Allow for dynamic fields from API
}

// Product creation data
export interface ProductCreateData {
  name: string;
  price: number;
  quantity: number;
  category: string;
  [key: string]: string | number;
}

// Product list response
export interface ProductsResponse {
  data: Product[];
}

// Transformed data response
export interface TransformedDataResponse {
  data: Product[];
}

// Aggregate response
export interface AggregateResponse {
  result: number;
} 