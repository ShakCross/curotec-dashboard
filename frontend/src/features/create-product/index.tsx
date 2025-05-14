import React, { useState } from 'react';
import { PlusIcon } from '@heroicons/react/24/outline';
import Input from '../../shared/ui/Input';
import SelectInput from '../../shared/ui/SelectInput';
import Button from '../../shared/ui/Button';
import Modal from '../../shared/ui/Modal';
import { PRODUCT_CATEGORIES } from '../../entities/product/constants';
import { CreateProductProvider, useCreateProduct } from './context';
import { Product } from '../../entities/product/model';
import './styles.css';

// Map categories to option format for SelectInput
const categoryOptions = PRODUCT_CATEGORIES.map(category => ({
  value: category,
  label: category,
}));

// Props for the form component
interface CreateProductFormProps {
  onProductCreated?: (product: Product) => void;
}

// The form component that uses the context
const CreateProductForm: React.FC<CreateProductFormProps> = ({ onProductCreated }) => {
  const { formData, setFormData, createProduct, status, error, product, resetForm } = useCreateProduct();
  
  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'number') {
      // For numeric inputs, handle empty string and invalid values
      if (value === '') {
        // Allow empty field during typing but store as 0
        setFormData({ [name]: 0 });
      } else {
        // Parse to appropriate numeric type
        const numericValue = name === 'quantity' 
          ? parseInt(value, 10) || 0 
          : parseFloat(value) || 0;
        
        setFormData({ [name]: numericValue });
      }
    } else {
      // For non-numeric inputs
      setFormData({ [name]: value });
    }
  };
  
  // Handle category selection
  const handleCategoryChange = (value: string) => {
    setFormData({ category: value });
  };
  
  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createProduct();
  };
  
  // Handle form reset
  const handleReset = () => {
    resetForm();
  };

  // Call the onProductCreated callback when the product is created
  React.useEffect(() => {
    if (status === 'success' && product && onProductCreated) {
      onProductCreated(product);
    }
  }, [status, product, onProductCreated]);
  
  // Get display values for form inputs (showing empty string instead of 0)
  const getPriceDisplay = () => {
    return formData.price === 0 ? '' : formData.price;
  };
  
  const getQuantityDisplay = () => {
    return formData.quantity === 0 ? '' : formData.quantity;
  };
  
  return (
    <form className="create-product-form" onSubmit={handleSubmit}>
      {status === 'error' && error && (
        <div className="create-product-form__error">
          {error}
        </div>
      )}
      
      {status === 'success' && product && (
        <div className="create-product-form__success">
          <p>Product created successfully!</p>
          <p>ID: {product.id}</p>
          <Button 
            type="button" 
            onClick={handleReset}
            className="mt-4"
          >
            Create Another Product
          </Button>
        </div>
      )}
      
      {status !== 'success' && (
        <>
          <div className="create-product-form__field">
            <Input
              label="Product Name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter product name"
              required
            />
          </div>
          
          <div className="create-product-form__field">
            <Input
              label="Price"
              name="price"
              type="number"
              value={getPriceDisplay()}
              onChange={handleChange}
              placeholder="0.00"
              min="0.01"
              step="0.01"
              required
            />
          </div>
          
          <div className="create-product-form__field">
            <Input
              label="Quantity"
              name="quantity"
              type="number"
              value={getQuantityDisplay()}
              onChange={handleChange}
              placeholder="0"
              min="1"
              step="1"
              required
            />
          </div>
          
          <div className="create-product-form__field">
            <SelectInput
              label="Category"
              options={categoryOptions}
              value={formData.category}
              onChange={handleCategoryChange}
              required
            />
          </div>
          
          <div className="create-product-form__actions">
            <Button
              type="submit"
              fullWidth
              isLoading={status === 'loading'}
              disabled={status === 'loading'}
            >
              Create Product
            </Button>
          </div>
        </>
      )}
    </form>
  );
};

// Main component props
interface CreateProductFeatureProps {
  onProductCreated?: (product: Product) => void;
}

// Main component that includes both the button and modal
const CreateProductFeature: React.FC<CreateProductFeatureProps> = ({ onProductCreated }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);
  
  return (
    <CreateProductProvider>
      <Button
        type="button"
        onClick={openModal}
        icon={<PlusIcon className="h-5 w-5" />}
      >
        Add New Product
      </Button>
      
      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        title="Create New Product"
      >
        <CreateProductForm onProductCreated={onProductCreated} />
      </Modal>
    </CreateProductProvider>
  );
};

export default CreateProductFeature; 