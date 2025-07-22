import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Brain, Upload, MessageSquare, BarChart3, Zap, Database, Cpu, Activity, TrendingUp, Shield, Rocket } from 'lucide-react';
import { getModelStatus } from '../services/api';
import { ModelStatus } from '../types';

const Dashboard: React.FC = () => {
  const [modelStatus, setModelStatus] = useState<ModelStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const status = await getModelStatus();
        setModelStatus(status);
      } catch (error) {
        console.error('Error fetching model status:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

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
        return <Brain className="h-5 w-5" />;
      case 'training':
        return <Cpu className="h-5 w-5 animate-spin" />;
      case 'error':
        return <Zap className="h-5 w-5" />;
      default:
        return <Database className="h-5 w-5" />;
    }
  };

  const quickActions = [
    {
      title: 'Entrenar Modelo',
      description: 'Sube archivos y entrena el UltraEfficientLLM',
      icon: Upload,
      path: '/training',
      color: 'bg-gradient-to-r from-blue-500 to-blue-600',
      bgColor: 'bg-blue-900/20',
      borderColor: 'border-blue-400/30',
      iconColor: 'text-blue-400',
    },
    {
      title: 'Chatbot IA',
      description: 'Chat inteligente con razonamiento paso a paso',
      icon: MessageSquare,
      path: '/chatbot',
      color: 'bg-gradient-to-r from-emerald-500 to-emerald-600',
      bgColor: 'bg-emerald-900/20',
      borderColor: 'border-emerald-400/30',
      iconColor: 'text-emerald-400',
      requiresModel: true,
    },
    {
      title: 'Ver Estado',
      description: 'Monitorea el estado y métricas del modelo',
      icon: BarChart3,
      path: '/status',
      color: 'bg-gradient-to-r from-purple-500 to-purple-600',
      bgColor: 'bg-purple-900/20',
      borderColor: 'border-purple-400/30',
      iconColor: 'text-purple-400',
    },
  ];

  const features = [
    {
      title: 'Ultra-Eficiente',
      description: 'Solo 13.6 MB vs 14GB de GPT',
      icon: Zap,
      bgColor: 'bg-blue-900/20',
      borderColor: 'border-blue-400/30',
      iconColor: 'text-blue-400',
    },
    {
      title: 'Razonamiento Transparente',
      description: 'Proceso interno observable',
      icon: Brain,
      bgColor: 'bg-emerald-900/20',
      borderColor: 'border-emerald-400/30',
      iconColor: 'text-emerald-400',
    },
    {
      title: 'Escalable',
      description: 'Maneja 10,000+ patrones',
      icon: TrendingUp,
      bgColor: 'bg-purple-900/20',
      borderColor: 'border-purple-400/30',
      iconColor: 'text-purple-400',
    },
    {
      title: 'Sparsity Extrema',
      description: '99.9% de patrones inactivos',
      icon: Shield,
      bgColor: 'bg-amber-900/20',
      borderColor: 'border-amber-400/30',
      iconColor: 'text-amber-400',
    },
  ];

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
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-indigo-600/20 to-purple-600/20 backdrop-blur-xl"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/80 to-slate-800/80"></div>
        <div className="relative z-10 text-center">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-gradient-to-br from-blue-500/20 to-indigo-500/20 rounded-2xl backdrop-blur-md border border-blue-400/30">
              <Rocket className="h-16 w-16 text-blue-400" />
            </div>
          </div>
          <h1 className="text-5xl font-bold mb-4 text-gradient text-shadow">
            UltraEfficientLLM Dashboard
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Interfaz web para entrenar y evaluar el modelo de lenguaje ultra-eficiente
          </p>
          <div className="mt-6 flex justify-center">
            <div className="flex items-center space-x-2 bg-slate-800/50 px-4 py-2 rounded-full backdrop-blur-sm border border-slate-600/50">
              <Activity className="h-4 w-4 text-blue-400" />
              <span className="text-slate-300 text-sm">Sistema de IA Avanzado</span>
            </div>
          </div>
        </div>
      </div>

      {/* Model Status Card con glassmorphism */}
      <div className="card card-highlight hover-lift">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-blue-500/20 rounded-xl backdrop-blur-sm border border-blue-400/30">
              <Brain className="h-8 w-8 text-blue-400" />
            </div>
            <h2 className="text-2xl font-bold text-blue-100">Estado del Modelo</h2>
          </div>
          {modelStatus && (
            <div className={`flex items-center space-x-2 px-4 py-2 rounded-full text-sm font-bold ${getStatusColor(modelStatus.status)}`}>
              {getStatusIcon(modelStatus.status)}
              <span className="capitalize">{modelStatus.status}</span>
            </div>
          )}
        </div>
        
        {modelStatus && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
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
              <div className="text-lg font-bold text-purple-400 mb-2">
                {modelStatus.message}
              </div>
              <div className="text-sm text-slate-300">Estado Actual</div>
            </div>
          </div>
        )}
      </div>

      {/* Quick Actions con glassmorphism */}
      <div className="card hover-lift">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-2 bg-emerald-500/20 rounded-lg backdrop-blur-sm border border-emerald-400/30">
            <Zap className="h-8 w-8 text-emerald-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">Acciones Rápidas</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action) => {
            const Icon = action.icon;
            const isDisabled = action.requiresModel && (!modelStatus || modelStatus.status !== 'trained');
            
            return (
              <Link
                key={action.path}
                to={action.path}
                className={`group block p-6 ${action.bgColor} border ${action.borderColor} rounded-xl hover:shadow-2xl transition-all duration-300 backdrop-blur-sm hover-lift ${
                  isDisabled ? 'opacity-50 cursor-not-allowed pointer-events-none' : ''
                }`}
              >
                <div className={`inline-flex p-3 rounded-lg text-white mb-4 ${action.color} ${isDisabled ? 'opacity-50' : ''}`}>
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className={`text-lg font-bold text-white mb-2 group-hover:${action.iconColor} transition-colors`}>
                  {action.title}
                </h3>
                <p className="text-slate-300">{action.description}</p>
                {isDisabled && (
                  <div className="mt-2 text-xs text-red-400 bg-red-900/20 px-2 py-1 rounded">
                    Requiere modelo entrenado
                  </div>
                )}
              </Link>
            );
          })}
        </div>
      </div>

      {/* Features con glassmorphism */}
      <div className="card hover-lift">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-2 bg-purple-500/20 rounded-lg backdrop-blur-sm border border-purple-400/30">
            <Database className="h-8 w-8 text-purple-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">Características Principales</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className={`text-center p-6 ${feature.bgColor} border ${feature.borderColor} rounded-xl backdrop-blur-sm hover-lift transition-all duration-300`}>
                <div className={`inline-flex p-3 ${feature.bgColor} rounded-lg ${feature.iconColor} mb-4 border ${feature.borderColor}`}>
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="font-bold text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-slate-300">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 