const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const login = async (credentials: { username: string; password: string }) => {
  const response = await fetch(`${API_URL}/auth/token/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });
  if (!response.ok) {
    throw new Error('Login failed');
  }
  return response.json();
};

export const register = async (userData: { username: string; email: string; password: string; first_name: string; last_name: string }) => {
  const response = await fetch(`${API_URL}/auth/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
  if (!response.ok) {
    throw new Error('Registration failed');
  }
  return response.json();
};

export const refreshToken = async (refresh: string) => {
  const response = await fetch(`${API_URL}/auth/token/refresh/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh }),
  });
  if (!response.ok) {
    throw new Error('Token refresh failed');
  }
  return response.json();
};