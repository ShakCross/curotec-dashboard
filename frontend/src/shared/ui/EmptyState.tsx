import React, { ReactNode } from 'react';

interface EmptyStateProps {
  message: string;
  action?: ReactNode;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  message,
  action,
  className = '',
}) => {
  return (
    <div className={`p-12 text-center text-gray-500 flex flex-col items-center gap-4 ${className}`}>
      <p>{message}</p>
      {action}
    </div>
  );
};

export default EmptyState; 