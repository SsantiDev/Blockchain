const API_URL = 'http://localhost:8001';

const authHeaders = () => {
  const token = localStorage.getItem('nc_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const getChain = () =>
  fetch(`${API_URL}/chain`);

export const notarize = (formData) =>
  fetch(`${API_URL}/notarize`, { method: 'POST', body: formData, headers: authHeaders() });

export const verify = (formData) =>
  fetch(`${API_URL}/verify`, { method: 'POST', body: formData });

export const login = (body) =>
  fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    body: JSON.stringify(body),
    headers: { 'Content-Type': 'application/json' },
  });

export const register = (body) =>
  fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    body: JSON.stringify(body),
    headers: { 'Content-Type': 'application/json' },
  });

export const getMe = () =>
  fetch(`${API_URL}/users/me`, { headers: authHeaders() });

export const getMyNotarizations = () =>
  fetch(`${API_URL}/my-notarizations`, { headers: authHeaders() });

export const getCertificate = (txHash) =>
  fetch(`${API_URL}/notarizations/${txHash}/certificate`, { headers: authHeaders() });
