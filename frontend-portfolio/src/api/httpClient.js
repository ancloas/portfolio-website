// src/api/httpClient.js
import config from '../config';

const defaultHeaders = {
  'Content-Type': 'application/json',
//   'x-api-key': config.apiKey, // optional custom header
};

const httpClient = async (url, options = {}) => {
  const fullUrl = `${config.baseUrl}${url}`;

  const response = await fetch(fullUrl, {
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`HTTP error! ${response.status} - ${errorBody}`);
  }

  return response.json();
};

export default httpClient;
