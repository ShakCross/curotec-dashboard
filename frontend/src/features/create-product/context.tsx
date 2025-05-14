import React, { createContext, useContext, useState, ReactNode } from 'react';
import { ProductCreateData, Product } from '../../entities/product/model';
import { createProduct } from './api';
import { ApiStatus } from '../../shared/types/common';

// Context state interface
interface CreateProductContextState {
  status: ApiStatus;
  error: string | null;
  product: Product | null;
  formData: ProductCreateData;
  createProduct: () => Promise<void>;
  setFormData: (data: Partial<ProductCreateData>) => void;
  resetForm: () => void;
}

// Initial form data
const initialFormData: ProductCreateData = {
  name: '',
  price: 0,
  quantity: 0,
  category: '',
};

// Create context with default values
const CreateProductContext = createContext<CreateProductContextState>({
  status: 'idle',
  error: null,
  product: null,
  formData: initialFormData,
  createProduct: async () => {},
  setFormData: () => {},
  resetForm: () => {},
});

// Provider component that wraps your app and makes auth object available to any
// child component that calls useCreateProduct().
export const CreateProductProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [status, setStatus] = useState<ApiStatus>('idle');
  const [error, setError] = useState<string | null>(null);
  const [product, setProduct] = useState<Product | null>(null);
  const [formData, setFormDataState] = useState<ProductCreateData>(initialFormData);

  // Update form data - fixed type error
  const setFormData = (data: Partial<ProductCreateData>) => {
    setFormDataState(prevState => {
      // Process numeric fields to ensure they're stored as numbers
      const updatedData = { ...data };
      
      // Handle price field specifically
      if ('price' in updatedData && typeof updatedData.price === 'string') {
        updatedData.price = parseFloat(updatedData.price) || 0;
      }
      
      // Handle quantity field specifically
      if ('quantity' in updatedData && typeof updatedData.quantity === 'string') {
        updatedData.quantity = parseInt(updatedData.quantity, 10) || 0;
      }
      
      // Create a safe copy without the index signature conflict
      const updatedState = {
        name: prevState.name,
        price: prevState.price,
        quantity: prevState.quantity,
        category: prevState.category,
        ...updatedData
      };
      
      return updatedState;
    });
  };

  // Reset form to initial state
  const resetForm = () => {
    setFormDataState(initialFormData);
    setStatus('idle');
    setError(null);
    setProduct(null);
  };

  // Create product
  const handleCreateProduct = async () => {
    try {
      setStatus('loading');
      setError(null);

      // Validate form data
      if (!formData.name.trim()) {
        throw new Error('Product name is required');
      }
      
      // Ensure price is a valid number and greater than 0
      const price = parseFloat(String(formData.price));
      if (isNaN(price) || price <= 0) {
        throw new Error('Price must be greater than 0');
      }
      
      // Ensure quantity is a valid number and greater than 0
      const quantity = parseInt(String(formData.quantity), 10);
      if (isNaN(quantity) || quantity <= 0) {
        throw new Error('Quantity must be greater than 0');
      }
      
      if (!formData.category.trim()) {
        throw new Error('Category is required');
      }

      // Prepare data with proper numeric types
      const productData: ProductCreateData = {
        ...formData,
        price: price,
        quantity: quantity
      };

      // Create product
      const createdProduct = await createProduct(productData);
      setProduct(createdProduct);
      setStatus('success');
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'Failed to create product');
    }
  };

  // Context value
  const value = {
    status,
    error,
    product,
    formData,
    createProduct: handleCreateProduct,
    setFormData,
    resetForm,
  };

  return (
    <CreateProductContext.Provider value={value}>
      {children}
    </CreateProductContext.Provider>
  );
};

// Hook to use the create product context
export const useCreateProduct = () => {
  return useContext(CreateProductContext);
}; 