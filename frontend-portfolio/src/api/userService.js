// src/api/userService.js
import httpClient from './httpClient';

export const getAllUsers = () => httpClient('/users');

export const getUserById = (id) => httpClient(`/users/${id}`);

export const createUser = (userData) =>
  httpClient('/users', {
    method: 'POST',
    body: JSON.stringify(userData),
  });

export const updateUser = (id, userData) =>
  httpClient(`/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  });

export const deleteUser = (id) =>
  httpClient(`/users/${id}`, {
    method: 'DELETE',
  });
