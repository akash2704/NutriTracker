import { describe, test, expect, beforeEach, vi } from 'vitest';
import * as api from '../api';

// Mock fetch
global.fetch = vi.fn();

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
});
