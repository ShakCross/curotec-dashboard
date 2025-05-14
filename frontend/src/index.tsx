// This is the main entry point for the React application
// It imports the App component from the app directory

import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './app/App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
); 