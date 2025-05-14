import React from 'react';
import { ShoppingCartIcon, TagIcon } from '@heroicons/react/24/outline';
import { Product } from '../../entities/product/model';
import { formatPrice, formatNumber } from '../../entities/product/utils';
import './styles.css';

interface ProductCardProps {
  product: Product;
  onClick?: (product: Product) => void;
  className?: string;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onClick,
  className = '',
}) => {
  const handleClick = () => {
    if (onClick) {
      onClick(product);
    }
  };
  
  // Ensure safe access to product properties
  const safeProduct = {
    ...product,
    price: product.price || 0,
    quantity: product.quantity || 0,
    name: product.name || 'Unnamed Product',
    category: product.category || 'Uncategorized',
    id: product.id || 0
  };
  
  // Calculate total inventory value
  const totalValue = safeProduct.price * safeProduct.quantity;
  
  return (
    <div 
      className={`product-card ${onClick ? 'cursor-pointer' : ''} ${className}`}
      onClick={onClick ? handleClick : undefined}
    >
      <div className="product-card__header">
        <span className="product-card__category">
          <TagIcon className="h-4 w-4 mr-1" />
          {safeProduct.category}
        </span>
        <span className="product-card__id">#{safeProduct.id}</span>
      </div>
      
      <h3 className="product-card__name">{safeProduct.name}</h3>
      
      <div className="product-card__info">
        <div className="product-card__price-info">
          <span className="product-card__price">{formatPrice(safeProduct.price)}</span>
          <span className="product-card__price-label">Price</span>
        </div>
        
        <div className="product-card__quantity-info">
          <span className="product-card__quantity">{formatNumber(safeProduct.quantity)}</span>
          <span className="product-card__quantity-label">In Stock</span>
        </div>
      </div>
      
      <div className="product-card__footer">
        <div className="product-card__total">
          <span className="product-card__total-label">Total value</span>
          <span className="product-card__total-value">{formatPrice(totalValue)}</span>
        </div>
        
        <div className="product-card__action">
          <ShoppingCartIcon className="h-5 w-5" />
        </div>
      </div>
    </div>
  );
};

export default ProductCard; 