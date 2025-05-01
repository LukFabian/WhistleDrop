import axios from 'axios';

let apiBaseUrl: string
if (import.meta.env.MODE === "development") {
  apiBaseUrl = "http://127.0.0.1:8000"
} else {
  apiBaseUrl = "http://YOUR_ONION_ADDRESS.onion:8000"
}
export const http = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10_000,
});

http.interceptors.request.use(cfg => {
  const token = localStorage.getItem('token');
  if (token) cfg.headers!.Authorization = `Bearer ${token}`;
  return cfg;
});
