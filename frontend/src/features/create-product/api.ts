import { postData } from '../../shared/lib/api';
import { Product, ProductCreateData } from '../../entities/product/model';
import { API_ENDPOINTS } from '../../shared/config/api';

/**
 * Create a new product by sending a POST request to the API
 * @param productData - The product data to create
 * @returns The created product
 */
export const createProduct = async (productData: ProductCreateData): Promise<Product> => {
  // Ensure all required fields exist and are non-empty
  const validatedData: ProductCreateData = {
    name: productData.name || 'Unnamed Product',
    price: typeof productData.price === 'number' ? productData.price : 0,
    quantity: typeof productData.quantity === 'number' ? productData.quantity : 0,
    category: productData.category || 'Uncategorized'
  };

  console.log('Sending product data to API:', validatedData);
  
  // API expects an array of products for batch creation
  return postData<Product[], ProductCreateData[]>(API_ENDPOINTS.PROCESS, [validatedData])
    .then(response => {
      // API returns an array of created products, we take the first one
      if (response && response.length > 0) {
        console.log('Received product from API:', response[0]);
        return response[0];
      }
      throw new Error('No product was returned from the API');
    });
}; 