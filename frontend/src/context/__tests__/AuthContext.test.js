import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../AuthContext';

// Mock API
jest.mock('../../services/api', () => ({
  getCurrentUser: jest.fn(),
}));

const TestComponent = () => {
  const { user, login, logout, loading } = useAuth();
  
  return (
    <div>
      <div data-testid="loading">{loading ? 'loading' : 'not-loading'}</div>
      <div data-testid="user">{user ? user.email : 'no-user'}</div>
      <button onClick={() => login('test@example.com', 'password')}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  test('provides initial state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('loading')).toHaveTextContent('not-loading');
    expect(screen.getByTestId('user')).toHaveTextContent('no-user');
  });

  test('handles login with token in localStorage', async () => {
    const mockUser = { email: 'test@example.com', id: 1 };
    localStorage.setItem('token', 'mock-token');
    
    const { getCurrentUser } = require('../../services/api');
    getCurrentUser.mockResolvedValue(mockUser);

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId('user')).toHaveTextContent('test@example.com');
    });
  });

  test('handles logout', async () => {
    localStorage.setItem('token', 'mock-token');
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    const logoutButton = screen.getByText('Logout');
    logoutButton.click();

    await waitFor(() => {
      expect(screen.getByTestId('user')).toHaveTextContent('no-user');
      expect(localStorage.removeItem).toHaveBeenCalledWith('token');
    });
  });
});
