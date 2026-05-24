import axios from 'axios';
import { Source, ChatResponse, Health } from '../types';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 120000, // la generación puede tardar unos segundos
});

export const getHealth = async (): Promise<Health> => {
  const response = await api.get('/health');
  return response.data;
};

export const listSources = async (): Promise<{ sources: Source[]; domain: string }> => {
  const response = await api.get('/sources');
  return response.data;
};

export const addSource = async (text: string): Promise<Source> => {
  const response = await api.post('/sources', { text });
  return response.data;
};

export const updateSource = async (id: string, text: string): Promise<Source> => {
  const response = await api.put(`/sources/${id}`, { text });
  return response.data;
};

export const deleteSource = async (id: string): Promise<{ deleted: string }> => {
  const response = await api.delete(`/sources/${id}`);
  return response.data;
};

export const uploadSources = async (file: File): Promise<{ added: number; sources: Source[] }> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/sources/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const chat = async (message: string, topK = 3): Promise<ChatResponse> => {
  const response = await api.post('/chat', { message, top_k: topK });
  return response.data;
};

export default api;
