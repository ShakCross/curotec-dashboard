import React from 'react';
import Button from './Button';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  onRetry,
  className = '',
}) => {
  return (
    <div className={`p-4 mb-6 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-center ${className}`}>
      {message}
      {onRetry && (
        <Button 
          variant="primary" 
          size="sm" 
          onClick={onRetry}
          className="ml-4"
        >
          Retry
        </Button>
      )}
    </div>
  );
};

export default ErrorMessage; 