// src/api/authService.js
import httpClient from './httpClient';

export const login = (credentials) =>
  httpClient('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });

// export const register = (userInfo) =>
//   httpClient('/auth/register', {
//     method: 'POST',
//     body: JSON.stringify(userInfo),
//   });

export const getCurrentUser = () => httpClient('/auth/me');
