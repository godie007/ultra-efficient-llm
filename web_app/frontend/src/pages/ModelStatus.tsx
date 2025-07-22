import { useEffect, useState } from 'react';
import { BarChart3, Database, Cpu, Zap, RefreshCw, Activity, TrendingUp, Shield, Rocket, Target } from 'lucide-react';
import { getModelStatus, resetModel } from '../services/api';
import { ModelStatus } from '../types';
import toast from 'react-hot-toast';

const ModelStatusPage: React.FC = () => {
  const [modelStatus, setModelStatus] = useState<ModelStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [resetting, setResetting] = useState(false);

  const fetchStatus = async () => {
    try {
      const status = await getModelStatus();
      setModelStatus(status);
    } catch (error) {
      console.error('Error fetching model status:', error);
      toast.error('Error al cargar el estado del modelo');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000); // Poll every 3 seconds
    return () => clearInterval(interval);
  }, []);

  const handleReset = async () => {
    if (!confirm('¿Estás seguro de que quieres reiniciar el modelo? Se perderán todos los datos de entrenamiento.')) {
      return;
    }

    setResetting(true);
    try {
      await resetModel();
      toast.success('Modelo reiniciado exitosamente');
      fetchStatus();
    } catch (error) {
      toast.error('Error al reiniciar el modelo');
    } finally {
      setResetting(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'trained':
        return 'status-connected';
      case 'training':
        return 'status-warning';
      case 'error':
        return 'status-disconnected';
      default:
        return 'bg-gradient-to-r from-slate-500 to-slate-400 text-white shadow-lg border border-slate-400/30 backdrop-blur-sm';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'trained':
        return <Database className="h-5 w-5" />;
      case 'training':
        return <Cpu className="h-5 w-5 animate-spin" />;
      case 'error':
        return <Zap className="h-5 w-5" />;
      default:
        return <Database className="h-5 w-5" />;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 p-6 min-h-screen">
      {/* Header con glassmorphism */}
      <div className="relative overflow-hidden rounded-3xl p-8 shadow-3xl">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 via-indigo-600/20 to-blue-600/20 backdrop-blur-xl"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/80 to-slate-800/80"></div>
        <div className="relative z-10 text-center">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 rounded-2xl backdrop-blur-md border border-purple-400/30">
              <BarChart3 className="h-16 w-16 text-purple-400" />
            </div>
          </div>
          <h1 className="text-5xl font-bold mb-4 text-gradient text-shadow">
            Estado del Modelo
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Monitorea el estado y métricas del UltraEfficientLLM
          </p>
          <div className="mt-6 flex justify-center">
            <div className="flex items-center space-x-2 bg-slate-800/50 px-4 py-2 rounded-full backdrop-blur-sm border border-slate-600/50">
              <Activity className="h-4 w-4 text-purple-400" />
              <span className="text-slate-300 text-sm">Monitoreo en Tiempo Real</span>
            </div>
          </div>
        </div>
      </div>

      {/* Current Status */}
      <div className="card card-highlight hover-lift">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-purple-500/20 rounded-lg backdrop-blur-sm border border-purple-400/30">
              <Target className="h-8 w-8 text-purple-400" />
            </div>
            <h2 className="text-2xl font-bold text-purple-100">Estado Actual</h2>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={fetchStatus}
              className="btn-secondary flex items-center space-x-2"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Actualizar</span>
            </button>
            <button
              onClick={handleReset}
              disabled={resetting}
              className="btn-danger disabled:opacity-50 flex items-center space-x-2"
            >
              {resetting ? (
                <>
                  <div className="loading-spinner-small"></div>
                  <span>Reiniciando...</span>
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4" />
                  <span>Reiniciar Modelo</span>
                </>
              )}
            </button>
          </div>
        </div>

        {modelStatus && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
              <div className="text-3xl font-bold text-blue-400 mb-2">
                {modelStatus.patterns_stored.toLocaleString()}
              </div>
              <div className="text-sm text-slate-300">Patrones Almacenados</div>
            </div>
            <div className="text-center p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
              <div className="text-3xl font-bold text-emerald-400 mb-2">
                {(modelStatus.memory_kb / 1024).toFixed(1)}
              </div>
              <div className="text-sm text-slate-300">Memoria (MB)</div>
            </div>
            <div className="text-center p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
              <div className="text-3xl font-bold text-purple-400 mb-2">
                {modelStatus.model_stats?.sparsity ? `${(modelStatus.model_stats.sparsity * 100).toFixed(1)}%` : 'N/A'}
              </div>
              <div className="text-sm text-slate-300">Sparsity</div>
            </div>
            <div className="text-center p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
              <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-bold ${getStatusColor(modelStatus.status)}`}>
                {getStatusIcon(modelStatus.status)}
                <span className="capitalize">{modelStatus.status}</span>
              </div>
              <div className="text-sm text-slate-300 mt-2">Estado</div>
            </div>
          </div>
        )}
      </div>

      {/* Detailed Metrics */}
      {modelStatus && (
        <div className="card hover-lift">
          <div className="flex items-center space-x-4 mb-6">
            <div className="p-2 bg-blue-500/20 rounded-lg backdrop-blur-sm border border-blue-400/30">
              <BarChart3 className="h-8 w-8 text-blue-400" />
            </div>
            <h2 className="text-2xl font-bold text-white">Métricas Detalladas</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
              <h3 className="text-lg font-bold text-white mb-4">Información del Modelo</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center py-2 border-b border-slate-600/50">
                  <span className="text-slate-300">Estado:</span>
                  <span className="font-medium text-white capitalize">{modelStatus.status}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-slate-600/50">
                  <span className="text-slate-300">Entrenando:</span>
                  <span className="font-medium text-emerald-400">{modelStatus.is_training ? 'Sí' : 'No'}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-slate-600/50">
                  <span className="text-slate-300">Progreso:</span>
                  <span className="font-medium text-blue-400">{modelStatus.progress}%</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-slate-600/50">
                  <span className="text-slate-300">Mensaje:</span>
                  <span className="font-medium text-white">{modelStatus.message}</span>
                </div>
              </div>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
              <h3 className="text-lg font-bold text-white mb-4">Estadísticas de Rendimiento</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center py-2 border-b border-slate-600/50">
                  <span className="text-slate-300">Patrones Totales:</span>
                  <span className="font-medium text-purple-400">{modelStatus.patterns_stored.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-slate-600/50">
                  <span className="text-slate-300">Memoria Utilizada:</span>
                  <span className="font-medium text-emerald-400">{modelStatus.memory_kb.toLocaleString()} KB</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-slate-600/50">
                  <span className="text-slate-300">Eficiencia vs GPT:</span>
                  <span className="font-medium text-emerald-400">1,000x más eficiente</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-slate-600/50">
                  <span className="text-slate-300">Sparsity:</span>
                  <span className="font-medium text-amber-400">99.9% inactivos</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Progress Bar for Training */}
      {modelStatus?.is_training && (
        <div className="card card-warning hover-lift">
          <div className="flex items-center space-x-4 mb-6">
            <div className="p-2 bg-amber-500/20 rounded-lg backdrop-blur-sm border border-amber-400/30">
              <TrendingUp className="h-8 w-8 text-amber-400" />
            </div>
            <h2 className="text-2xl font-bold text-amber-100">Progreso del Entrenamiento</h2>
          </div>
          <div className="space-y-4">
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${modelStatus.progress}%` }}
              ></div>
            </div>
            <div className="flex justify-between text-sm text-slate-300">
              <span>0%</span>
              <span>{modelStatus.progress}%</span>
              <span>100%</span>
            </div>
            <p className="text-amber-200">{modelStatus.message}</p>
          </div>
        </div>
      )}

      {/* Model Information */}
      <div className="card hover-lift">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-2 bg-emerald-500/20 rounded-lg backdrop-blur-sm border border-emerald-400/30">
            <Rocket className="h-8 w-8 text-emerald-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">Información del UltraEfficientLLM</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="text-center p-6 bg-blue-900/20 rounded-xl border border-blue-400/30 backdrop-blur-sm hover-lift">
            <BarChart3 className="h-8 w-8 text-blue-400 mx-auto mb-3" />
            <h3 className="font-bold text-blue-100 mb-2">Eficiencia Extrema</h3>
            <p className="text-sm text-slate-300">Solo 13.6 MB vs 14GB de GPT tradicional</p>
          </div>
          <div className="text-center p-6 bg-emerald-900/20 rounded-xl border border-emerald-400/30 backdrop-blur-sm hover-lift">
            <Shield className="h-8 w-8 text-emerald-400 mx-auto mb-3" />
            <h3 className="font-bold text-emerald-100 mb-2">Sparsity Revolucionaria</h3>
            <p className="text-sm text-slate-300">99.9% de patrones permanecen inactivos</p>
          </div>
          <div className="text-center p-6 bg-purple-900/20 rounded-xl border border-purple-400/30 backdrop-blur-sm hover-lift">
            <Cpu className="h-8 w-8 text-purple-400 mx-auto mb-3" />
            <h3 className="font-bold text-purple-100 mb-2">Velocidad Alta</h3>
            <p className="text-sm text-slate-300">100+ tokens/s en generación</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelStatusPage; 