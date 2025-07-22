import { useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, Trash2, Play, Settings, RefreshCw, Wifi, WifiOff, Zap, Brain, Database, Cpu, Activity, Save } from 'lucide-react';
import toast from 'react-hot-toast';
import { uploadFile, listFiles, deleteFile, trainModel, getModelStatus, saveModel } from '../services/api';
import { UploadedFile, TrainingConfig } from '../types';

const Training: React.FC = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const [training, setTraining] = useState(false);
  const [loading, setLoading] = useState(false);
  const [modelStatus, setModelStatus] = useState<any>(null);
  const [backendConnected, setBackendConnected] = useState(false);
  const [saving, setSaving] = useState(false);
  const [newModelName, setNewModelName] = useState('');
  const [config, setConfig] = useState<TrainingConfig>({
    max_patterns: 10000,
    max_pattern_length: 8,
    min_frequency: 1,
  });

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'text/*': ['.txt', '.md'],
      'application/json': ['.json'],
      'text/csv': ['.csv'],
    },
    onDrop: async (acceptedFiles) => {
      console.log('🔄 Archivos aceptados:', acceptedFiles);
      
      if (!backendConnected) {
        toast.error('Backend no está conectado. Inicia el servidor backend primero.');
        return;
      }
      
      if (acceptedFiles.length === 0) {
        toast.error('No se seleccionaron archivos válidos');
        return;
      }

      setLoading(true);
      
      try {
        for (const file of acceptedFiles) {
          try {
            console.log('📤 Subiendo archivo:', file.name, 'Tamaño:', file.size);
            const result = await uploadFile(file);
            console.log('✅ Resultado de subida:', result);
            toast.success(`Archivo ${file.name} subido exitosamente`);
          } catch (error: any) {
            console.error('❌ Error al subir archivo:', error);
            const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
            toast.error(`Error al subir ${file.name}: ${errorMessage}`);
          }
        }
        
        // Esperar un poco y luego actualizar la lista
        console.log('⏳ Esperando para actualizar lista...');
        setTimeout(async () => {
          try {
            await fetchFiles();
            console.log('✅ Lista actualizada después de subida');
          } catch (error) {
            console.error('❌ Error al actualizar lista después de subida:', error);
          } finally {
            setLoading(false);
          }
        }, 1000);
      } catch (error) {
        console.error('❌ Error general en proceso de subida:', error);
        setLoading(false);
      }
    },
  });

  const checkBackendConnection = async () => {
    try {
      console.log('🔍 Verificando conexión con el backend...');
      const response = await fetch('http://localhost:8001/api/health', { 
        method: 'GET',
        signal: AbortSignal.timeout(3000000) // 30 segundos timeout
      });
      
      if (response.ok) {
        console.log('✅ Backend conectado');
        setBackendConnected(true);
        return true;
      } else {
        console.log('❌ Backend no responde correctamente');
        setBackendConnected(false);
        return false;
      }
    } catch (error) {
      console.log('❌ Backend no está disponible:', error);
      setBackendConnected(false);
      return false;
    }
  };

  const fetchFiles = async () => {
    if (!backendConnected) {
      console.log('⚠️ Backend no conectado, saltando fetchFiles');
      return;
    }

    try {
      console.log('📁 Solicitando lista de archivos...');
      const response = await listFiles();
      console.log('📋 Respuesta de archivos:', response);
      
      if (response && response.files) {
        setFiles(response.files);
        console.log('📝 Archivos actualizados en estado:', response.files);
      } else {
        console.warn('⚠️ Respuesta inesperada:', response);
        setFiles([]);
      }
    } catch (error: any) {
      console.error('❌ Error al cargar archivos:', error);
      if (error.code === 'ECONNABORTED') {
        toast.error('Timeout: El backend no responde. Verifica que esté ejecutándose.');
        setBackendConnected(false);
      } else {
        const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
        toast.error(`Error al cargar archivos: ${errorMessage}`);
      }
      setFiles([]);
    }
  };

  const fetchModelStatus = async () => {
    if (!backendConnected) {
      return;
    }

    try {
      const status = await getModelStatus();
      setModelStatus(status);
    } catch (error: any) {
      console.error('Error fetching model status:', error);
      if (error.code === 'ECONNABORTED') {
        setBackendConnected(false);
      }
    }
  };

  useEffect(() => {
    console.log('🚀 Componente Training montado');
    
    // Verificar conexión al montar
    checkBackendConnection().then((connected) => {
      if (connected) {
        fetchFiles();
        fetchModelStatus();
      }
    });

    // Verificar conexión cada 10 segundos
    const connectionInterval = setInterval(checkBackendConnection, 10000);
    
    // Actualizar estado del modelo cada 5 segundos solo si está conectado
    const statusInterval = setInterval(() => {
      if (backendConnected) {
        fetchModelStatus();
      }
    }, 5000);

    return () => {
      clearInterval(connectionInterval);
      clearInterval(statusInterval);
    };
  }, [backendConnected]);

  const handleDeleteFile = async (filename: string) => {
    if (!backendConnected) {
      toast.error('Backend no está conectado');
      return;
    }

    try {
      console.log('🗑️ Eliminando archivo:', filename);
      await deleteFile(filename);
      toast.success('Archivo eliminado');
      await fetchFiles();
      setSelectedFiles(selectedFiles.filter(f => f !== filename));
    } catch (error: any) {
      console.error('❌ Error al eliminar archivo:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
      toast.error(`Error al eliminar archivo: ${errorMessage}`);
    }
  };

  const handleTrain = async () => {
    if (!backendConnected) {
      toast.error('Backend no está conectado');
      return;
    }

    if (selectedFiles.length === 0) {
      toast.error('Selecciona al menos un archivo para entrenar');
      return;
    }

    setTraining(true);
    try {
      console.log('🎯 Iniciando entrenamiento con archivos:', selectedFiles);
      const result = await trainModel(selectedFiles, config);
      toast.success('Entrenamiento completado exitosamente');
      console.log('Training result:', result);
    } catch (error: any) {
      console.error('❌ Error durante el entrenamiento:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
      toast.error(`Error durante el entrenamiento: ${errorMessage}`);
    } finally {
      setTraining(false);
    }
  };

  const handleSaveModel = async () => {
    if (!backendConnected) {
      toast.error('Backend no está conectado');
      return;
    }

    if (!newModelName.trim()) {
      toast.error('Ingresa un nombre para el modelo');
      return;
    }

    if (!modelStatus?.is_trained) {
      toast.error('No hay un modelo entrenado para guardar');
      return;
    }

    setSaving(true);
    try {
      console.log('💾 Guardando modelo:', newModelName);
      const result = await saveModel(newModelName);
      toast.success('Modelo guardado exitosamente');
      console.log('Save result:', result);
      setNewModelName('');
    } catch (error: any) {
      console.error('❌ Error al guardar modelo:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
      toast.error(`Error al guardar modelo: ${errorMessage}`);
    } finally {
      setSaving(false);
    }
  };

  const toggleFileSelection = (filename: string) => {
    setSelectedFiles(prev => 
      prev.includes(filename) 
        ? prev.filter(f => f !== filename)
        : [...prev, filename]
    );
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleRefreshFiles = async () => {
    console.log('🔄 Refrescando archivos manualmente...');
    setLoading(true);
    try {
      await fetchFiles();
      console.log('✅ Archivos refrescados manualmente');
    } catch (error) {
      console.error('❌ Error al refrescar archivos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReconnectBackend = async () => {
    console.log('🔄 Intentando reconectar con el backend...');
    const connected = await checkBackendConnection();
    if (connected) {
      toast.success('Backend reconectado exitosamente');
      await fetchFiles();
      await fetchModelStatus();
    } else {
      toast.error('No se pudo conectar con el backend');
    }
  };

  // Debug: Mostrar información del estado
  console.log('🔍 Estado actual - files:', files);
  console.log('🔍 Estado actual - selectedFiles:', selectedFiles);
  console.log('🔍 Estado actual - loading:', loading);
  console.log('🔍 Estado actual - backendConnected:', backendConnected);

  return (
    <div className="space-y-8 p-6 min-h-screen">
      {/* Header con glassmorphism y gradiente profesional */}
      <div className="relative overflow-hidden rounded-3xl p-8 shadow-3xl">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-indigo-600/20 to-purple-600/20 backdrop-blur-xl"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/80 to-slate-800/80"></div>
        <div className="relative z-10 text-center">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-gradient-to-br from-blue-500/20 to-indigo-500/20 rounded-2xl backdrop-blur-md border border-blue-400/30">
              <Brain className="h-16 w-16 text-blue-400" />
            </div>
          </div>
          <h1 className="text-5xl font-bold mb-4 text-gradient text-shadow">Entrenamiento del Modelo</h1>
          <p className="text-xl text-slate-300">
            Sube archivos de texto y entrena el UltraEfficientLLM
          </p>
          <div className="mt-6 flex justify-center">
            <div className="flex items-center space-x-2 bg-slate-800/50 px-4 py-2 rounded-full backdrop-blur-sm border border-slate-600/50">
              <Cpu className="h-4 w-4 text-blue-400" />
              <span className="text-slate-300 text-sm">Sistema de IA Avanzado</span>
            </div>
          </div>
        </div>
      </div>

      {/* Connection Status con glassmorphism */}
      <div className={`card ${backendConnected ? 'card-success' : 'card-error'} hover-lift`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className={`p-3 rounded-xl ${backendConnected ? 'bg-emerald-500/20' : 'bg-red-500/20'} backdrop-blur-sm border ${backendConnected ? 'border-emerald-400/30' : 'border-red-400/30'}`}>
              {backendConnected ? (
                <Wifi className="h-8 w-8 text-emerald-400" />
              ) : (
                <WifiOff className="h-8 w-8 text-red-400" />
              )}
            </div>
            <div>
              <h3 className={`text-2xl font-bold ${backendConnected ? 'text-emerald-100' : 'text-red-100'}`}>
                Estado de Conexión
              </h3>
              <p className={`text-sm ${backendConnected ? 'text-emerald-300' : 'text-red-300'}`}>
                {backendConnected ? 'Comunicación establecida' : 'Sin conexión al servidor'}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className={backendConnected ? 'status-connected' : 'status-disconnected'}>
              {backendConnected ? 'Conectado' : 'Desconectado'}
            </span>
            {!backendConnected && (
              <button 
                onClick={handleReconnectBackend}
                className="btn-primary flex items-center space-x-2"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Reconectar</span>
              </button>
            )}
          </div>
        </div>
        {!backendConnected && (
          <div className="mt-6 p-4 bg-red-900/50 rounded-xl border border-red-500/30 backdrop-blur-sm">
            <p className="text-red-200 font-medium">
              El backend no está disponible. Asegúrate de que esté ejecutándose en http://localhost:8001
            </p>
            <p className="text-red-300 text-sm mt-2">
              Comando: cd web_app/backend && python simple_main.py
            </p>
          </div>
        )}
      </div>

      {/* Debug Info con diseño de dashboard */}
      <div className="card card-warning hover-lift">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-amber-500/20 rounded-lg backdrop-blur-sm border border-amber-400/30">
              <Zap className="h-6 w-6 text-amber-400" />
            </div>
            <h3 className="text-xl font-bold text-amber-100">Panel de Control</h3>
          </div>
          <button 
            onClick={handleRefreshFiles}
            disabled={loading || !backendConnected}
            className="btn-secondary flex items-center space-x-2 disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refrescar</span>
          </button>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 backdrop-blur-sm">
            <div className="flex items-center space-x-2 mb-2">
              <Activity className="h-4 w-4 text-emerald-400" />
              <p className="text-sm font-bold text-slate-300">Backend</p>
            </div>
            <p className="text-lg font-bold text-emerald-100">{backendConnected ? 'Conectado' : 'Desconectado'}</p>
          </div>
          <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 backdrop-blur-sm">
            <div className="flex items-center space-x-2 mb-2">
              <Database className="h-4 w-4 text-blue-400" />
              <p className="text-sm font-bold text-slate-300">Archivos</p>
            </div>
            <p className="text-lg font-bold text-blue-100">{files.length}</p>
          </div>
          <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 backdrop-blur-sm">
            <div className="flex items-center space-x-2 mb-2">
              <File className="h-4 w-4 text-purple-400" />
              <p className="text-sm font-bold text-slate-300">Seleccionados</p>
            </div>
            <p className="text-lg font-bold text-purple-100">{selectedFiles.length}</p>
          </div>
          <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 backdrop-blur-sm">
            <div className="flex items-center space-x-2 mb-2">
              <Settings className="h-4 w-4 text-slate-400" />
              <p className="text-sm font-bold text-slate-300">Estado</p>
            </div>
            <p className="text-lg font-bold text-slate-100">{loading ? 'Cargando...' : 'Listo'}</p>
          </div>
        </div>
        {files.length > 0 && (
          <div className="mt-6 p-4 bg-amber-900/30 rounded-xl border border-amber-500/30 backdrop-blur-sm">
            <p className="text-sm font-bold text-amber-200 mb-3">Archivos disponibles:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {files.map((file, index) => (
                <div key={index} className="flex items-center space-x-2 text-xs text-amber-300">
                  <File className="h-3 w-3" />
                  <span className="font-medium">{file.filename}</span>
                  <span className="text-amber-400">({formatFileSize(file.size_bytes)})</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Model Status con diseño avanzado */}
      {modelStatus && backendConnected && (
        <div className="card card-highlight hover-lift">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-blue-500/20 rounded-xl backdrop-blur-sm border border-blue-400/30">
                <Brain className="h-8 w-8 text-blue-400" />
              </div>
              <h2 className="text-2xl font-bold text-blue-100">Estado del Modelo</h2>
            </div>
            <div className={`px-4 py-2 rounded-full text-sm font-bold ${
              modelStatus.status === 'trained' ? 'status-connected' :
              modelStatus.status === 'training' ? 'status-warning' :
              'bg-gradient-to-r from-slate-500 to-slate-400 text-white shadow-lg border border-slate-400/30 backdrop-blur-sm'
            }`}>
              {modelStatus.status === 'training' && (
                <div className="loading-spinner-small inline-block mr-2"></div>
              )}
              {modelStatus.status}
            </div>
          </div>
          {modelStatus.is_training && (
            <div className="space-y-4">
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ width: `${modelStatus.progress}%` }}
                ></div>
              </div>
              <p className="text-blue-200 font-medium">{modelStatus.message}</p>
            </div>
          )}
        </div>
      )}

      {/* File Upload con glassmorphism */}
      <div className="card hover-lift">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-2 bg-blue-500/20 rounded-lg backdrop-blur-sm border border-blue-400/30">
            <Upload className="h-8 w-8 text-blue-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">Subir Archivos</h2>
        </div>
        <div
          {...getRootProps()}
          className={`border-3 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 backdrop-blur-sm ${
            isDragActive ? 'border-blue-500 bg-blue-900/30 shadow-2xl' : 'border-slate-600 hover:border-blue-500 hover:shadow-xl bg-slate-800/30'
          } ${loading || !backendConnected ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <input {...getInputProps()} disabled={loading || !backendConnected} />
          <Upload className="mx-auto h-16 w-16 text-slate-400 mb-6" />
          {!backendConnected ? (
            <div>
              <p className="text-red-400 text-xl font-bold">Backend no conectado</p>
              <p className="text-slate-400 mt-2">Inicia el servidor backend primero</p>
            </div>
          ) : loading ? (
            <div>
              <div className="loading-spinner mx-auto mb-4"></div>
              <p className="text-blue-400 text-xl font-bold">Procesando archivos...</p>
              <p className="text-slate-400 mt-2">Esto puede tomar unos segundos</p>
            </div>
          ) : isDragActive ? (
            <p className="text-blue-400 text-xl font-bold">Suelta los archivos aquí...</p>
          ) : (
            <div>
              <p className="text-slate-300 mb-3 text-lg">
                Arrastra archivos aquí, o <span className="text-blue-400 font-bold">haz clic para seleccionar</span>
              </p>
              <p className="text-slate-400">
                Formatos soportados: .txt, .md, .json, .csv
              </p>
            </div>
          )}
        </div>
      </div>

      {/* File List con diseño de tabla moderna */}
      <div className="card hover-lift">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-purple-500/20 rounded-lg backdrop-blur-sm border border-purple-400/30">
              <Database className="h-8 w-8 text-purple-400" />
            </div>
            <h2 className="text-2xl font-bold text-white">
              Archivos Subidos ({files.length})
            </h2>
          </div>
          {loading && (
            <div className="flex items-center space-x-2 text-sm text-slate-400">
              <div className="loading-spinner-small"></div>
              <span>Actualizando...</span>
            </div>
          )}
        </div>
        
        {!backendConnected ? (
          <div className="text-center py-12 text-slate-400">
            <div className="p-4 bg-slate-800/50 rounded-2xl backdrop-blur-sm border border-slate-600/50 inline-block mb-4">
              <WifiOff className="h-16 w-16 text-slate-500" />
            </div>
            <p className="text-xl font-bold">Backend no conectado</p>
            <p className="text-slate-500">Conecta el backend para ver los archivos</p>
          </div>
        ) : files.length === 0 ? (
          <div className="text-center py-12 text-slate-400">
            <div className="p-4 bg-slate-800/50 rounded-2xl backdrop-blur-sm border border-slate-600/50 inline-block mb-4">
              <File className="h-16 w-16 text-slate-500" />
            </div>
            <p className="text-xl font-bold">No hay archivos subidos</p>
            <p className="text-slate-500">Sube archivos para comenzar el entrenamiento</p>
            {loading && (
              <div className="mt-6">
                <div className="loading-spinner mx-auto"></div>
                <p className="text-slate-500 mt-2">Verificando archivos...</p>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {files.map((file) => (
              <div
                key={file.filename}
                className={`flex items-center justify-between p-6 border-2 rounded-xl transition-all duration-300 hover-lift backdrop-blur-sm ${
                  selectedFiles.includes(file.filename)
                    ? 'border-blue-500 bg-blue-900/30 shadow-lg'
                    : 'border-slate-600 hover:border-slate-500 hover:shadow-md bg-slate-800/30'
                }`}
              >
                <div className="flex items-center space-x-4">
                  <input
                    type="checkbox"
                    checked={selectedFiles.includes(file.filename)}
                    onChange={() => toggleFileSelection(file.filename)}
                    className="checkbox-custom"
                  />
                  <div className="p-2 bg-slate-700/50 rounded-lg backdrop-blur-sm border border-slate-600/50">
                    <File className="h-8 w-8 text-slate-400" />
                  </div>
                  <div>
                    <p className="font-bold text-white text-lg">{file.filename}</p>
                    <p className="text-sm text-slate-400">
                      {formatFileSize(file.size_bytes)} • {new Date(file.uploaded_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteFile(file.filename)}
                  className="btn-danger p-3"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Training Configuration con diseño de formulario profesional */}
      <div className="card hover-lift">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-2 bg-emerald-500/20 rounded-lg backdrop-blur-sm border border-emerald-400/30">
            <Settings className="h-8 w-8 text-emerald-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">Configuración de Entrenamiento</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-bold text-slate-300 mb-3">
              Máximo de Patrones
            </label>
            <input
              type="number"
              value={config.max_patterns}
              onChange={(e) => setConfig(prev => ({ ...prev, max_patterns: parseInt(e.target.value) }))}
              className="input-field"
              min="1000"
              max="50000"
            />
          </div>
          <div>
            <label className="block text-sm font-bold text-slate-300 mb-3">
              Longitud Máxima de Patrón
            </label>
            <input
              type="number"
              value={config.max_pattern_length}
              onChange={(e) => setConfig(prev => ({ ...prev, max_pattern_length: parseInt(e.target.value) }))}
              className="input-field"
              min="3"
              max="15"
            />
          </div>
          <div>
            <label className="block text-sm font-bold text-slate-300 mb-3">
              Frecuencia Mínima
            </label>
            <input
              type="number"
              value={config.min_frequency}
              onChange={(e) => setConfig(prev => ({ ...prev, min_frequency: parseInt(e.target.value) }))}
              className="input-field"
              min="1"
              max="10"
            />
          </div>
        </div>
      </div>

      {/* Train Button con diseño destacado */}
      <div className="card card-highlight hover-lift">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-blue-100 mb-2">Entrenar Modelo</h2>
            <p className="text-blue-200">
              {!backendConnected ? 'Backend no conectado' :
               selectedFiles.length > 0 
                ? `${selectedFiles.length} archivo(s) seleccionado(s)`
                : 'Selecciona archivos para entrenar'
              }
            </p>
          </div>
          <button
            onClick={handleTrain}
            disabled={selectedFiles.length === 0 || training || loading || !backendConnected}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-3 text-lg"
          >
            {training ? (
              <>
                <div className="loading-spinner"></div>
                <span>Entrenando...</span>
              </>
            ) : (
              <>
                <Play className="h-6 w-6" />
                <span>Entrenar Modelo</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Save Model Section */}
      {modelStatus?.is_trained && backendConnected && (
        <div className="card hover-lift">
          <div className="flex items-center space-x-4 mb-6">
            <div className="p-2 bg-green-500/20 rounded-lg backdrop-blur-sm border border-green-400/30">
              <Save className="h-8 w-8 text-green-400" />
            </div>
            <h2 className="text-2xl font-bold text-white">Guardar Modelo Entrenado</h2>
          </div>
          <div className="flex items-center space-x-4">
            <input
              type="text"
              value={newModelName}
              onChange={(e) => setNewModelName(e.target.value)}
              placeholder="Nombre del modelo (ej: mi_modelo_español)"
              className="input-field flex-1"
              disabled={saving}
            />
            <button
              onClick={handleSaveModel}
              disabled={!newModelName.trim() || saving || !backendConnected}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {saving ? (
                <>
                  <div className="loading-spinner"></div>
                  <span>Guardando...</span>
                </>
              ) : (
                <>
                  <Save className="h-5 w-5" />
                  <span>Guardar</span>
                </>
              )}
            </button>
          </div>
          <p className="text-sm text-slate-400 mt-3">
            💡 Guarda tu modelo entrenado para reutilizarlo más tarde sin necesidad de volver a entrenar
          </p>
        </div>
      )}
    </div>
  );
};

export default Training; 