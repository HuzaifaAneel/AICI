import axios from 'axios';

const API_URL = 'http://localhost:8080';


interface User {
  user_id: string;
  email: string;
}
interface LoginResponse {
  access_token: string;
  user: User;
}

export const login = async (email: string, password: string): Promise<LoginResponse> => {
  try {
    const response = await axios.post<LoginResponse>(`${API_URL}/auth/login`, { email, password });
    return response.data;
  } catch (error: any) {
    throw error.response?.data?.detail || "An error occurred while logging in";
  }
};

export const register = async (email: string, password: string): Promise<void> => {
  try {
    await axios.post(`${API_URL}/auth/register`, { email, password });
  } catch (error: any) {
    throw error.response.data.detail;
  }
};
