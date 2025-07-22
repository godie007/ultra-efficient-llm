import { useState, useEffect } from 'react';
import { Save, Download, Trash2, RefreshCw, Wifi, WifiOff, Brain, Database, HardDrive, Upload, CheckCircle, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import { listModels, saveModel, loadModel, deleteModel, getModelStatus } from '../services/api';
import { SavedModel, ModelStatus } from '../types';

const ModelManagement: React.FC = () => {
  const [models, setModels] = useState<SavedModel[]>([]);
  const [modelStatus, setModelStatus] = useState<ModelStatus | null>(null);
  const [backendConnected, setBackendConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [loadingModel, setLoadingModel] = useState<string | null>(null);
  const [newModelName, setNewModelName] = useState('');

  const checkBackendConnection = async () => {
    try {
      console.log('🔍 Verificando conexión con el backend...');
      const response = await fetch('http://localhost:8001/api/health', { 
        method: 'GET',
        signal: AbortSignal.timeout(3000)
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

  const fetchModels = async () => {
    if (!backendConnected) {
      console.log('⚠️ Backend no conectado, saltando fetchModels');
      return;
    }

    try {
      console.log('📁 Solicitando lista de modelos...');
      const response = await listModels();
      console.log('📋 Respuesta de modelos:', response);
      
      if (response && response.models) {
        setModels(response.models);
        console.log('📝 Modelos actualizados en estado:', response.models);
      } else {
        console.warn('⚠️ Respuesta inesperada:', response);
        setModels([]);
      }
    } catch (error: any) {
      console.error('❌ Error al cargar modelos:', error);
      if (error.code === 'ECONNABORTED') {
        toast.error('Timeout: El backend no responde. Verifica que esté ejecutándose.');
        setBackendConnected(false);
      } else {
        const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
        toast.error(`Error al cargar modelos: ${errorMessage}`);
      }
      setModels([]);
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
    console.log('🚀 Componente ModelManagement montado');
    
    // Verificar conexión al montar
    checkBackendConnection().then((connected) => {
      if (connected) {
        fetchModels();
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
      await fetchModels();
    } catch (error: any) {
      console.error('❌ Error al guardar modelo:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
      toast.error(`Error al guardar modelo: ${errorMessage}`);
    } finally {
      setSaving(false);
    }
  };

  const handleLoadModel = async (modelFilename: string) => {
    if (!backendConnected) {
      toast.error('Backend no está conectado');
      return;
    }

    setLoadingModel(modelFilename);
    try {
      console.log('📂 Cargando modelo:', modelFilename);
      const result = await loadModel(modelFilename);
      toast.success('Modelo cargado exitosamente');
      console.log('Load result:', result);
      await fetchModelStatus();
    } catch (error: any) {
      console.error('❌ Error al cargar modelo:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
      toast.error(`Error al cargar modelo: ${errorMessage}`);
    } finally {
      setLoadingModel(null);
    }
  };

  const handleDeleteModel = async (modelFilename: string) => {
    if (!backendConnected) {
      toast.error('Backend no está conectado');
      return;
    }

    if (!confirm(`¿Estás seguro de que quieres eliminar el modelo "${modelFilename}"?`)) {
      return;
    }

    try {
      console.log('🗑️ Eliminando modelo:', modelFilename);
      await deleteModel(modelFilename);
      toast.success('Modelo eliminado exitosamente');
      await fetchModels();
    } catch (error: any) {
      console.error('❌ Error al eliminar modelo:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Error desconocido';
      toast.error(`Error al eliminar modelo: ${errorMessage}`);
    }
  };

  const handleRefreshModels = async () => {
    console.log('🔄 Refrescando modelos manualmente...');
    setLoading(true);
    try {
      await fetchModels();
      console.log('✅ Modelos refrescados manualmente');
    } catch (error) {
      console.error('❌ Error al refrescar modelos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReconnectBackend = async () => {
    console.log('🔄 Intentando reconectar con el backend...');
    const connected = await checkBackendConnection();
    if (connected) {
      toast.success('Backend reconectado exitosamente');
      await fetchModels();
      await fetchModelStatus();
    } else {
      toast.error('No se pudo conectar con el backend');
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-8 p-6 min-h-screen">
      {/* Header con glassmorphism y gradiente profesional */}
      <div className="relative overflow-hidden rounded-3xl p-8 shadow-3xl">
        <div className="absolute inset-0 bg-gradient-to-br from-green-600/20 via-emerald-600/20 to-teal-600/20 backdrop-blur-xl"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/80 to-slate-800/80"></div>
        <div className="relative z-10 text-center">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-2xl backdrop-blur-md border border-green-400/30">
              <HardDrive className="h-16 w-16 text-green-400" />
            </div>
          </div>
          <h1 className="text-5xl font-bold mb-4 text-gradient text-shadow">Gestión de Modelos</h1>
          <p className="text-xl text-slate-300">
            Guarda, carga y gestiona modelos entrenados previamente
          </p>
          <div className="mt-6 flex justify-center">
            <div className="flex items-center space-x-2 bg-slate-800/50 px-4 py-2 rounded-full backdrop-blur-sm border border-slate-600/50">
              <Brain className="h-4 w-4 text-green-400" />
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
              Comando: cd web_app/backend && python main.py
            </p>
          </div>
        )}
      </div>

      {/* Current Model Status */}
      {modelStatus && backendConnected && (
        <div className="card card-highlight hover-lift">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-blue-500/20 rounded-xl backdrop-blur-sm border border-blue-400/30">
                <Brain className="h-8 w-8 text-blue-400" />
              </div>
              <h2 className="text-2xl font-bold text-blue-100">Modelo Actual</h2>
            </div>
            <div className={`px-4 py-2 rounded-full text-sm font-bold ${
              modelStatus.is_trained ? 'status-connected' :
              modelStatus.status === 'training' ? 'status-warning' :
              'bg-gradient-to-r from-slate-500 to-slate-400 text-white shadow-lg border border-slate-400/30 backdrop-blur-sm'
            }`}>
              {modelStatus.is_trained ? (
                <div className="flex items-center space-x-2">
                  <CheckCircle className="h-4 w-4" />
                  <span>Entrenado</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <AlertCircle className="h-4 w-4" />
                  <span>No Entrenado</span>
                </div>
              )}
            </div>
          </div>
          {modelStatus.is_trained && modelStatus.model_info && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 backdrop-blur-sm">
                <div className="flex items-center space-x-2 mb-2">
                  <Database className="h-4 w-4 text-blue-400" />
                  <p className="text-sm font-bold text-slate-300">Patrones</p>
                </div>
                <p className="text-lg font-bold text-blue-100">{modelStatus.model_info.patterns_count}</p>
              </div>
              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 backdrop-blur-sm">
                <div className="flex items-center space-x-2 mb-2">
                  <Brain className="h-4 w-4 text-purple-400" />
                  <p className="text-sm font-bold text-slate-300">Embeddings</p>
                </div>
                <p className="text-lg font-bold text-purple-100">{modelStatus.model_info.word_vectors_count}</p>
              </div>
              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 backdrop-blur-sm">
                <div className="flex items-center space-x-2 mb-2">
                  <HardDrive className="h-4 w-4 text-emerald-400" />
                  <p className="text-sm font-bold text-slate-300">Memoria</p>
                </div>
                <p className="text-lg font-bold text-emerald-100">{modelStatus.model_info.memory_usage_kb.toFixed(1)} KB</p>
              </div>
              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-600/50 backdrop-blur-sm">
                <div className="flex items-center space-x-2 mb-2">
                  <Database className="h-4 w-4 text-amber-400" />
                  <p className="text-sm font-bold text-slate-300">Nodos</p>
                </div>
                <p className="text-lg font-bold text-amber-100">{modelStatus.model_info.pattern_graph_nodes}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Save Current Model */}
      {modelStatus?.is_trained && backendConnected && (
        <div className="card hover-lift">
          <div className="flex items-center space-x-4 mb-6">
            <div className="p-2 bg-green-500/20 rounded-lg backdrop-blur-sm border border-green-400/30">
              <Save className="h-8 w-8 text-green-400" />
            </div>
            <h2 className="text-2xl font-bold text-white">Guardar Modelo Actual</h2>
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
        </div>
      )}

      {/* Models List */}
      <div className="card hover-lift">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-purple-500/20 rounded-lg backdrop-blur-sm border border-purple-400/30">
              <Database className="h-8 w-8 text-purple-400" />
            </div>
            <h2 className="text-2xl font-bold text-white">
              Modelos Guardados ({models.length})
            </h2>
          </div>
          <button 
            onClick={handleRefreshModels}
            disabled={loading || !backendConnected}
            className="btn-secondary flex items-center space-x-2 disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refrescar</span>
          </button>
        </div>
        
        {!backendConnected ? (
          <div className="text-center py-12 text-slate-400">
            <div className="p-4 bg-slate-800/50 rounded-2xl backdrop-blur-sm border border-slate-600/50 inline-block mb-4">
              <WifiOff className="h-16 w-16 text-slate-500" />
            </div>
            <p className="text-xl font-bold">Backend no conectado</p>
            <p className="text-slate-500">Conecta el backend para ver los modelos</p>
          </div>
        ) : models.length === 0 ? (
          <div className="text-center py-12 text-slate-400">
            <div className="p-4 bg-slate-800/50 rounded-2xl backdrop-blur-sm border border-slate-600/50 inline-block mb-4">
              <HardDrive className="h-16 w-16 text-slate-500" />
            </div>
            <p className="text-xl font-bold">No hay modelos guardados</p>
            <p className="text-slate-500">Entrena un modelo y guárdalo para verlo aquí</p>
            {loading && (
              <div className="mt-6">
                <div className="loading-spinner mx-auto"></div>
                <p className="text-slate-500 mt-2">Verificando modelos...</p>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {models.map((model) => (
              <div
                key={model.filename}
                className="flex items-center justify-between p-6 border-2 rounded-xl transition-all duration-300 hover-lift backdrop-blur-sm border-slate-600 hover:border-slate-500 hover:shadow-md bg-slate-800/30"
              >
                <div className="flex items-center space-x-4">
                  <div className="p-2 bg-slate-700/50 rounded-lg backdrop-blur-sm border border-slate-600/50">
                    <HardDrive className="h-8 w-8 text-slate-400" />
                  </div>
                  <div>
                    <p className="font-bold text-white text-lg">{model.model_name}</p>
                    <p className="text-sm text-slate-400">
                      {formatFileSize(model.size_bytes)} • {new Date(model.created_at).toLocaleDateString()}
                    </p>
                    <p className="text-xs text-slate-500">{model.filename}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleLoadModel(model.filename)}
                    disabled={loadingModel === model.filename || !backendConnected}
                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                  >
                    {loadingModel === model.filename ? (
                      <>
                        <div className="loading-spinner-small"></div>
                        <span>Cargando...</span>
                      </>
                    ) : (
                      <>
                        <Download className="h-4 w-4" />
                        <span>Cargar</span>
                      </>
                    )}
                  </button>
                  <button
                    onClick={() => handleDeleteModel(model.filename)}
                    disabled={loadingModel === model.filename || !backendConnected}
                    className="btn-danger p-3 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Trash2 className="h-5 w-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ModelManagement; 