# Product Management Frontend

A modern React application for product management with a clean architecture, built with TypeScript and Tailwind CSS.

## Architecture

This project follows a feature-based architecture with clear separation of concerns:

- **app/** - Application setup, routing, and global providers
- **entities/** - Domain models and entity-specific components
- **features/** - Feature-specific components with business logic
- **pages/** - Page components that compose features and widgets
- **shared/** - Reusable components, hooks, utilities, and configurations
- **widgets/** - Composite UI blocks
- **styles/** - Global styles and Tailwind configuration

### Key Technologies

- React 18 with TypeScript
- React Router for navigation
- Axios for API integration
- Tailwind CSS for styling
- Context API for state management
- Custom hooks for reusable logic
- localStorage-based caching for API responses
- Real-time data updates with polling

## Features

- **Product Management**
  - View product listings with filtering and sorting
  - Create new products with form validation
  - Data visualization for product metrics
  - Responsive design for all device sizes
  - Real-time data updates with configurable polling

- **Clean Architecture**
  - Separation of UI, business logic, and data layers
  - Reusable components and hooks
  - Type safety with TypeScript
  - Consistent error handling and loading states

- **Client-side Caching**
  - API responses are cached in localStorage
  - Configurable cache expiration times
  - Automatic cache invalidation for modified data
  - Force refresh option for time-critical data

- **Real-time Updates**
  - Automatic data polling at configurable intervals
  - User controls to enable/disable real-time updates
  - Visual indicator for active polling
  - Smart updates that maintain current sorting/filtering

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server
npm run start
```

This runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Building for Production

```bash
# Build for production
npm run build
```

This builds the app for production to the `build` folder, optimized for best performance.

### Testing

```bash
# Run tests
npm test
```

## Project Structure

```
src/
├── app/                # Application setup
│   ├── App.tsx         # Main app component with routing
│   └── providers/      # Context providers
├── entities/           # Business entities
│   └── product/        # Product entity
│       ├── model.ts    # Type definitions
│       ├── ui/         # Entity-specific UI components
│       ├── hooks/      # Entity-specific hooks
│       │   ├── useProducts.ts       # Basic products hook
│       │   └── usePollingProducts.ts # Products with real-time updates
│       └── utils.ts    # Entity-specific utilities
├── features/           # Feature modules
│   └── create-product/ # Product creation feature
│       ├── api.ts      # API integration
│       ├── context.tsx # Feature-specific state
│       └── index.tsx   # Feature components
├── pages/              # Application pages
├── shared/             # Shared code
│   ├── config/         # Configuration
│   ├── hooks/          # Custom hooks
│   │   ├── useFetch.ts # Basic data fetching hook
│   │   ├── usePolling.ts # Real-time polling hook
│   │   └── useToggle.ts # Toggle state hook
│   ├── lib/            # Utility libraries
│   │   ├── api.ts      # API client with caching
│   │   └── cache.ts    # Cache utility
│   ├── types/          # Common TypeScript types
│   └── ui/             # Reusable UI components
├── styles/             # Global styles
└── widgets/            # Composite UI blocks
    └── ProductCard/    # Product card widget
```

## API Integration

The frontend connects to a Django backend API at `http://localhost:8000/api`. Key endpoints:

- `GET /api/data/products/` - Retrieve all products
- `POST /api/data/process/` - Create new products
- `GET /api/data/transform/filter/` - Filter products
- `GET /api/data/transform/sort/` - Sort products
- `GET /api/data/transform/aggregate/` - Aggregate product data

## Caching Strategy

The application implements a client-side caching strategy using localStorage:

- **Cache Duration**: Default cache time is 5 minutes, configurable per request
- **Cache Keys**: Generated based on URL and request parameters
- **Cache Invalidation**: Cache is automatically invalidated when data is modified
- **Force Refresh**: API calls can bypass cache with the `forceRefresh` option
- **Selective Caching**: Some operations (like filtering/sorting) don't use cache by default

### Cache Configuration

The caching behavior can be customized through the `FetchOptions` interface:

```typescript
interface FetchOptions {
  useCache?: boolean;      // Whether to use cache (default: true)
  cacheTime?: number;      // Cache expiration time in minutes (default: 5)
  forceRefresh?: boolean;  // Force refresh cache even if not expired
}
```

## Real-time Updates

The application implements real-time data updates using polling:

- **Configurable Intervals**: Default polling interval is 10 seconds, configurable per component
- **User Controls**: Users can enable/disable real-time updates
- **Visual Feedback**: Active polling is indicated with a pulsing indicator
- **Smart Updates**: Updates preserve current sorting and filtering
- **Efficient Refreshes**: Only refreshes the data that has changed

### Polling Configuration

The polling behavior can be customized through the `PollingOptions` interface:

```typescript
interface PollingOptions {
  interval?: number;       // Polling interval in milliseconds (default: 10000)
  autoStart?: boolean;     // Whether polling should start immediately (default: true)
  runImmediately?: boolean; // Whether to run the first fetch immediately (default: true)
  enabled?: boolean;       // Whether polling is enabled (default: true)
}
```

## Error Handling

The application implements comprehensive error handling:

- Form validation with user-friendly messages
- API error handling with retry capabilities
- Loading states for asynchronous operations
- Empty state handling for lists and search results
