import React from 'react';
import { Product } from '../model';
import ProductCard from '../../../widgets/ProductCard';
import LoadingState from '../../../shared/ui/LoadingState';
import ErrorMessage from '../../../shared/ui/ErrorMessage';
import EmptyState from '../../../shared/ui/EmptyState';

interface ProductGridProps {
  products: Product[];
  loading: boolean;
  error: string | null;
  emptyAction?: React.ReactNode;
  onRetry?: () => void;
  className?: string;
}

export const ProductGrid: React.FC<ProductGridProps> = ({
  products,
  loading,
  error,
  emptyAction,
  onRetry,
  className = '',
}) => {
  if (loading) {
    return <LoadingState message="Loading products..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={onRetry} />;
  }

  if (products.length === 0) {
    return <EmptyState message="No products found." action={emptyAction} />;
  }

  return (
    <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 ${className}`}>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};

export default ProductGrid; 