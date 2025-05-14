import { useState, useCallback } from 'react';

/**
 * Custom hook for toggling a boolean state
 * @param initialState - Initial toggle state
 */
export function useToggle(initialState: boolean = false): [boolean, () => void, (value: boolean) => void] {
  const [state, setState] = useState<boolean>(initialState);
  
  // Toggle the state
  const toggle = useCallback(() => {
    setState(prev => !prev);
  }, []);
  
  // Set the state to a specific value
  const setValue = useCallback((value: boolean) => {
    setState(value);
  }, []);
  
  return [state, toggle, setValue];
}

export default useToggle; 