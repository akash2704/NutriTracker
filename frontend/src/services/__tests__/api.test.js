import * as api from '../api';

// Mock fetch
global.fetch = jest.fn();

describe('API Service', () => {
  beforeEach(() => {
    fetch.mockClear();
    localStorage.clear();
  });

  describe('register', () => {
    test('makes POST request to register endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'User registered successfully' }),
      });

      const result = await api.register('test@example.com', 'password123');

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/register'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: 'test@example.com',
            password: 'password123',
          }),
        })
      );
      expect(result).toEqual({ message: 'User registered successfully' });
    });

    test('throws error on failed registration', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Email already registered' }),
      });

      await expect(api.register('test@example.com', 'password123'))
        .rejects.toThrow('Email already registered');
    });
  });

  describe('login', () => {
    test('makes POST request to login endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ access_token: 'mock-token', token_type: 'bearer' }),
      });

      const result = await api.login('test@example.com', 'password123');

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/login'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'username=test%40example.com&password=password123',
        })
      );
      expect(result).toEqual({ access_token: 'mock-token', token_type: 'bearer' });
    });
  });

  describe('getCurrentUser', () => {
    test('makes GET request with authorization header', async () => {
      localStorage.setItem('token', 'mock-token');
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, email: 'test@example.com' }),
      });

      const result = await api.getCurrentUser();

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/users/me'),
        expect.objectContaining({
          headers: { 'Authorization': 'Bearer mock-token' },
        })
      );
      expect(result).toEqual({ id: 1, email: 'test@example.com' });
    });

    test('throws error when no token', async () => {
      await expect(api.getCurrentUser()).rejects.toThrow('No token found');
    });
  });

  describe('searchFoods', () => {
    test('makes GET request to foods endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => [{ id: 1, name: 'Rice' }],
      });

      const result = await api.searchFoods('rice', 10);

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/foods/?search=rice&limit=10')
      );
      expect(result).toEqual([{ id: 1, name: 'Rice' }]);
    });
  });

  describe('getRecommendations', () => {
    test('makes GET request with authorization', async () => {
      localStorage.setItem('token', 'mock-token');
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ bmr: 1500, tdee: 2000 }),
      });

      const result = await api.getRecommendations();

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/recommendations/'),
        expect.objectContaining({
          headers: { 'Authorization': 'Bearer mock-token' },
        })
      );
      expect(result).toEqual({ bmr: 1500, tdee: 2000 });
    });
  });
});
