import axios from 'axios';
import type { ProcessedDocument } from '../types/document';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1',
});

export const checkHealth = async () => {
  const { data } = await apiClient.get('/health');
  return data;
};

export const scanDocumentImage = async (file: File): Promise<ProcessedDocument> => {
  const formData = new FormData();
  formData.append('image', file);

  const { data } = await apiClient.post<ProcessedDocument>('/documents/scan', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return data;
};

export const listDocuments = async (): Promise<ProcessedDocument[]> => {
  const { data } = await apiClient.get<ProcessedDocument[]>('/documents');
  return data;
};

export const getDocumentById = async (id: string): Promise<ProcessedDocument> => {
  const { data } = await apiClient.get<ProcessedDocument>(`/documents/${id}`);
  return data;
};

export const deleteDocumentById = async (id: string): Promise<{ message: string }> => {
  const { data } = await apiClient.delete<{ message: string }>(`/documents/${id}`);
  return data;
};
