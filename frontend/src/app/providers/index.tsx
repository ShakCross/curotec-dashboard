import React from 'react';
import { CreateProductProvider } from '../../features/create-product/context';

interface AppProvidersProps {
  children: React.ReactNode;
}

/**
 * Application providers wrapper component
 * This component wraps the app with all required context providers
 */
export const AppProviders: React.FC<AppProvidersProps> = ({ children }) => {
  return (
    <CreateProductProvider>
      {children}
    </CreateProductProvider>
  );
};

export default AppProviders;
