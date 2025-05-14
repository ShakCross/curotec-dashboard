import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppProviders from './providers';
import Home from '../pages/Home';
import Products from '../pages/Products';
import '../styles/index.css';

/**
 * Main application component that provides routing
 * and global context providers
 */
export const App: React.FC = () => {
  return (
    <AppProviders>
      <BrowserRouter>
        <div className="app">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<Products />} />
          </Routes>
        </div>
      </BrowserRouter>
    </AppProviders>
  );
};

export default App;
