// src/config.js
const config = {
//   apiKey: import.meta.env.VITE_API_KEY,
  baseUrl: import.meta.env.VITE_BASE_URL,
};

export default config;
// This file contains the configuration for the application, including API keys and base URLs.
// It uses environment variables to keep sensitive information secure.  




// Use it like
// import config from '../config';

// fetch(`${config.baseUrl}/data?apiKey=${config.apiKey}`)
//   .then(res => res.json())
//   .then(data => console.log(data));
// This allows you to easily change the API key or base URL without modifying the code directly.
// This file is used to store configuration settings for the application.