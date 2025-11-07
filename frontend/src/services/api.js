import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ;

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  verify: (data) => api.post('/auth/verify', data),
  login: (data) => api.post('/auth/token', data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
};

export const userAPI = {
  getProfile: () => api.get('/users/me'),
  createProfile: (data) => api.post('/profile/me', data),
  getUserProfile: () => api.get('/profile/me'),
};

export const foodAPI = {
  searchFoods: (query, limit = 10) => api.get(`/foods/search?q=${query}&limit=${limit}`),
  getFoods: (skip = 0, limit = 20) => api.get(`/foods/?skip=${skip}&limit=${limit}`),
  getFood: (id) => api.get(`/foods/${id}`),
};

export const logAPI = {
  createLog: (data) => api.post('/food-logs/', data),
  getDashboard: (date) => api.get(`/dashboard/?log_date=${date}`),
};

export default api;
