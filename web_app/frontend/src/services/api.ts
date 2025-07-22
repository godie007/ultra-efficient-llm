import axios from 'axios';
import { ModelStatus, UploadedFile, TrainingResult, GenerationResult, TrainingConfig } from '../types';

// Configuración de la API - Usar URL directa al backend
const API_BASE_URL = 'http://localhost:8001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 segundos de timeout
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response: any) => {
    console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`);
    return response;
  },
  (error: any) => {
    console.error('🚨 Error en API:', error);
    if (error.code === 'ECONNABORTED') {
      console.error('⏰ Timeout en petición API');
    }
    if (error.response) {
      console.error(`📊 Status: ${error.response.status} - ${error.response.statusText}`);
      console.error('📄 Response data:', error.response.data);
    }
    return Promise.reject(error);
  }
);

// Interceptor para requests
api.interceptors.request.use(
  (config: any) => {
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    console.log('📍 Base URL:', config.baseURL);
    return config;
  },
  (error: any) => {
    console.error('❌ Error en request:', error);
    return Promise.reject(error);
  }
);

// Health check
export const healthCheck = async () => {
  try {
    console.log('🏥 Iniciando health check...');
    const response = await api.get('/health');
    console.log('✅ Health check exitoso:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error en health check:', error);
    throw error;
  }
};

// Model status
export const getModelStatus = async (): Promise<ModelStatus> => {
  try {
    console.log('📊 Obteniendo estado del modelo...');
    const response = await api.get('/model/status');
    console.log('✅ Estado del modelo obtenido:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error obteniendo estado del modelo:', error);
    throw error;
  }
};

// File upload
export const uploadFile = async (file: File) => {
  try {
    console.log('📤 Iniciando subida de archivo:', file.name);
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 3000000, // 30 segundos para subida de archivos
    });
    
    console.log('✅ Archivo subido exitosamente:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error subiendo archivo:', error);
    throw error;
  }
};

// List uploaded files
export const listFiles = async (): Promise<{ files: UploadedFile[] }> => {
  try {
    console.log('📁 Solicitando lista de archivos...');
    const response = await api.get('/files');
    console.log('📋 Respuesta de archivos recibida:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error listando archivos:', error);
    throw error;
  }
};

// Delete file
export const deleteFile = async (filename: string) => {
  try {
    console.log('🗑️ Eliminando archivo:', filename);
    const response = await api.delete(`/files/${filename}`);
    console.log('✅ Archivo eliminado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error eliminando archivo:', error);
    throw error;
  }
};

// Train model
export const trainModel = async (
  files: string[],
  config: TrainingConfig
): Promise<TrainingResult> => {
  try {
    console.log('🎯 Iniciando entrenamiento con archivos:', files);
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    formData.append('max_patterns', config.max_patterns.toString());
    formData.append('max_pattern_length', config.max_pattern_length.toString());
    formData.append('min_frequency', config.min_frequency.toString());
    
    const response = await api.post('/train', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60 segundos para entrenamiento
    });
    
    console.log('✅ Entrenamiento completado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error en entrenamiento:', error);
    throw error;
  }
};

// Generate text
export const generateText = async (
  prompt: string,
  maxLength: number = 20,
  temperature: number = 0.7,
  intelligentMode: boolean = true
): Promise<GenerationResult> => {
  try {
    console.log('🎨 Generando texto con prompt:', prompt, 'Modo inteligente:', intelligentMode);
    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('max_length', maxLength.toString());
    formData.append('temperature', temperature.toString());
    formData.append('intelligent_mode', intelligentMode.toString());
    
    const response = await api.post('/generate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 3000000, // 30 segundos para generación
    });
    
    console.log('✅ Texto generado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error generando texto:', error);
    throw error;
  }
};

// Reset model
export const resetModel = async () => {
  try {
    console.log('🔄 Reiniciando modelo...');
    const response = await api.post('/reset');
    console.log('✅ Modelo reiniciado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error reiniciando modelo:', error);
    throw error;
  }
};

// Nuevas funciones para gestión de modelos

// List saved models
export const listModels = async (): Promise<{ models: any[] }> => {
  try {
    console.log('📁 Solicitando lista de modelos...');
    const response = await api.get('/models');
    console.log('📋 Respuesta de modelos recibida:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error listando modelos:', error);
    throw error;
  }
};

// Save model
export const saveModel = async (modelName: string) => {
  try {
    console.log('💾 Guardando modelo:', modelName);
    const formData = new FormData();
    formData.append('model_name', modelName);
    
    const response = await api.post('/models/save', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // 30 segundos para guardar
    });
    
    console.log('✅ Modelo guardado exitosamente:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error guardando modelo:', error);
    throw error;
  }
};

// Load model
export const loadModel = async (modelFilename: string) => {
  try {
    console.log('📂 Cargando modelo:', modelFilename);
    const formData = new FormData();
    formData.append('model_filename', modelFilename);
    
    const response = await api.post('/models/load', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // 30 segundos para cargar
    });
    
    console.log('✅ Modelo cargado exitosamente:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error cargando modelo:', error);
    throw error;
  }
};

// Delete model
export const deleteModel = async (modelFilename: string) => {
  try {
    console.log('🗑️ Eliminando modelo:', modelFilename);
    const response = await api.delete(`/models/${modelFilename}`);
    console.log('✅ Modelo eliminado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error eliminando modelo:', error);
    throw error;
  }
};

// Analyze question with reasoning
export const analyzeQuestion = async (question: string) => {
  try {
    console.log('🧠 Analizando pregunta:', question);
    const formData = new FormData();
    formData.append('question', question);
    
    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    console.log('✅ Análisis completado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error analizando pregunta:', error);
    throw error;
  }
};

// Chatbot reasoning function
export const chatbotReasoning = async (
  prompt: string,
  maxLength: number = 20,
  temperature: number = 0.7,
  reasoningDepth: number = 3,
  responseStyle: string = "detailed"
) => {
  try {
    console.log('🤖 Iniciando chatbot reasoning:', prompt);
    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('max_length', maxLength.toString());
    formData.append('temperature', temperature.toString());
    formData.append('reasoning_depth', reasoningDepth.toString());
    formData.append('response_style', responseStyle);
    
    const response = await api.post('/chatbot-reasoning', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60 segundos para chatbot reasoning
    });
    
    console.log('✅ Chatbot reasoning completado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error en chatbot reasoning:', error);
    throw error;
  }
};

export default api; 