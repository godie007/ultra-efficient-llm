import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Send, Bot, User, Brain, Target, Zap, Clock, CheckCircle, Settings, Sliders, Gauge, Sparkles, Upload } from 'lucide-react';
import { chatbotReasoning, getModelStatus } from '../services/api';
import MarkdownRenderer from '../components/MarkdownRenderer';

interface ChatMessage {
  type: 'user' | 'system' | 'analysis' | 'reasoning' | 'base_response' | 'reasoned_response' | 'final_response' | 'patterns';
  content: string;
  timestamp: string;
  isTyping?: boolean;
}

const ChatbotReasoning: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  const [modelStatus, setModelStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [parameters, setParameters] = useState({
    maxLength: 50,
    temperature: 0.7,
    reasoningDepth: 3,
    responseStyle: 'detailed'
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const fetchModelStatus = async () => {
      try {
        const status = await getModelStatus();
        setModelStatus(status);
      } catch (error) {
        console.error('Error fetching model status:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchModelStatus();
  }, []);

  const getMessageIcon = (type: string) => {
    switch (type) {
      case 'user':
        return <User className="h-5 w-5 text-blue-400" />;
      case 'system':
        return <Bot className="h-5 w-5 text-purple-400" />;
      case 'analysis':
        return <Brain className="h-5 w-5 text-yellow-400" />;
      case 'reasoning':
        return <Target className="h-5 w-5 text-green-400" />;
      case 'base_response':
        return <Zap className="h-5 w-5 text-orange-400" />;
      case 'reasoned_response':
        return <Brain className="h-5 w-5 text-emerald-400" />;
      case 'final_response':
        return <CheckCircle className="h-5 w-5 text-blue-500" />;
      case 'patterns':
        return <Target className="h-5 w-5 text-purple-400" />;
      default:
        return <Bot className="h-5 w-5 text-gray-400" />;
    }
  };

  const getMessageStyle = (type: string) => {
    switch (type) {
      case 'user':
        return 'bg-blue-500/20 border-blue-400/30 text-blue-100';
      case 'system':
        return 'bg-purple-500/20 border-purple-400/30 text-purple-100';
      case 'analysis':
        return 'bg-yellow-500/20 border-yellow-400/30 text-yellow-100';
      case 'reasoning':
        return 'bg-green-500/20 border-green-400/30 text-green-100';
      case 'base_response':
        return 'bg-orange-500/20 border-orange-400/30 text-orange-100';
      case 'reasoned_response':
        return 'bg-emerald-500/20 border-emerald-400/30 text-emerald-100';
      case 'final_response':
        return 'bg-blue-500/20 border-blue-400/30 text-blue-100';
      case 'patterns':
        return 'bg-purple-500/20 border-purple-400/30 text-purple-100';
      default:
        return 'bg-gray-500/20 border-gray-400/30 text-gray-100';
    }
  };

  const simulateTyping = async (chatbotMessages: any[]) => {
    // Agregar mensaje del usuario
    setMessages(prev => [...prev, {
      type: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    }]);

    // Simular typing para cada mensaje del chatbot
    for (let i = 0; i < chatbotMessages.length; i++) {
      const message = chatbotMessages[i];
      
      // Agregar indicador de typing
      setMessages(prev => [...prev, {
        type: message.type,
        content: '',
        timestamp: message.timestamp,
        isTyping: true
      }]);

      // Simular delay de typing (más rápido para mejor UX)
      await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));

      // Reemplazar con el mensaje completo
      setMessages(prev => prev.map((msg, index) => 
        index === prev.length - 1 
          ? { ...message, isTyping: false }
          : msg
      ));

      setCurrentStep(i + 1);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isProcessing) return;

    // Verificar si hay un modelo entrenado
    if (!modelStatus || modelStatus.status !== 'trained') {
      setMessages(prev => [...prev, {
        type: 'system',
        content: '❌ **Error:** No hay un modelo entrenado disponible. Por favor, entrena un modelo primero en la sección de Entrenamiento.',
        timestamp: new Date().toISOString()
      }]);
      return;
    }

    // Activar estado de procesamiento
    setIsProcessing(true);
    setCurrentStep(0);

    try {
      const result = await chatbotReasoning(
        inputValue, 
        parameters.maxLength, 
        parameters.temperature,
        parameters.reasoningDepth,
        parameters.responseStyle
      );
      await simulateTyping(result.chatbot_messages);
      setInputValue('');
    } catch (error) {
      console.error('Error en chatbot reasoning:', error);
      setMessages(prev => [...prev, {
        type: 'system',
        content: '❌ Error al procesar la pregunta. Intenta de nuevo.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      // Desactivar estado de procesamiento
      setIsProcessing(false);
      setCurrentStep(0);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4 relative">
      {/* Indicador de progreso en la parte superior */}
      {isProcessing && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
          <div className="bg-slate-800/95 border border-orange-500/30 rounded-xl p-4 backdrop-blur-md shadow-2xl">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Brain className="h-6 w-6 text-orange-400 animate-pulse" />
                <div className="absolute inset-0 rounded-full border-2 border-orange-400/20 border-t-orange-400 animate-spin"></div>
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-orange-300">Procesando Razonamiento</span>
                  <span className="text-xs text-orange-400/70">Paso {currentStep} de 7</span>
                </div>
                <div className="w-48 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-orange-500 to-red-500 h-1.5 rounded-full transition-all duration-500"
                    style={{ width: `${(currentStep / 7) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-4 mb-4">
            <div className="p-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white">Chatbot de Razonamiento Inteligente</h1>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 bg-slate-700/50 rounded-lg border border-slate-600/50 hover:bg-slate-600/50 transition-colors"
              title="Configurar parámetros"
            >
              <Settings className="h-5 w-5 text-slate-300" />
            </button>
          </div>
          <p className="text-slate-300 text-lg mb-2">
            Ve el proceso de razonamiento paso a paso en tiempo real
          </p>
          {modelStatus && (
            <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${
              modelStatus.status === 'trained' 
                ? 'bg-green-500/20 text-green-400 border border-green-400/30' 
                : 'bg-red-500/20 text-red-400 border border-red-400/30'
            }`}>
              {modelStatus.status === 'trained' ? (
                <>
                  <CheckCircle className="h-4 w-4" />
                  <span>Modelo Disponible</span>
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4" />
                  <span>Modelo No Disponible</span>
                </>
              )}
            </div>
          )}
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="mb-6 bg-slate-800/50 rounded-2xl border border-slate-600/50 backdrop-blur-sm p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Sliders className="h-6 w-6 text-purple-400" />
              <h3 className="text-xl font-bold text-white">Configuración de Parámetros</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Max Length */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  <Gauge className="h-4 w-4 inline mr-2" />
                  Longitud Máxima
                </label>
                <input
                  type="range"
                  min="10"
                  max="100"
                  value={parameters.maxLength}
                  onChange={(e) => setParameters(prev => ({ ...prev, maxLength: parseInt(e.target.value) }))}
                  className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
                />
                <div className="flex justify-between text-xs text-slate-400 mt-1">
                  <span>10</span>
                  <span className="text-purple-400 font-medium">{parameters.maxLength}</span>
                  <span>100</span>
                </div>
              </div>

              {/* Temperature */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  <Sparkles className="h-4 w-4 inline mr-2" />
                  Temperatura
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="2.0"
                  step="0.1"
                  value={parameters.temperature}
                  onChange={(e) => setParameters(prev => ({ ...prev, temperature: parseFloat(e.target.value) }))}
                  className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
                />
                <div className="flex justify-between text-xs text-slate-400 mt-1">
                  <span>0.1</span>
                  <span className="text-purple-400 font-medium">{parameters.temperature}</span>
                  <span>2.0</span>
                </div>
              </div>

              {/* Reasoning Depth */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  <Target className="h-4 w-4 inline mr-2" />
                  Profundidad de Razonamiento
                </label>
                <select
                  value={parameters.reasoningDepth}
                  onChange={(e) => setParameters(prev => ({ ...prev, reasoningDepth: parseInt(e.target.value) }))}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value={1}>Básico (1 paso)</option>
                  <option value={2}>Intermedio (2 pasos)</option>
                  <option value={3}>Detallado (3 pasos)</option>
                  <option value={4}>Avanzado (4 pasos)</option>
                  <option value={5}>Completo (5 pasos)</option>
                </select>
              </div>

              {/* Response Style */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  <Zap className="h-4 w-4 inline mr-2" />
                  Estilo de Respuesta
                </label>
                <select
                  value={parameters.responseStyle}
                  onChange={(e) => setParameters(prev => ({ ...prev, responseStyle: e.target.value }))}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="concise">Concisa</option>
                  <option value="detailed">Detallada</option>
                  <option value="technical">Técnica</option>
                  <option value="educational">Educativa</option>
                  <option value="creative">Creativa</option>
                </select>
              </div>
            </div>

            <div className="mt-4 p-3 bg-slate-700/50 rounded-lg">
              <p className="text-sm text-slate-300">
                <strong>Configuración actual:</strong> Longitud {parameters.maxLength}, 
                Temperatura {parameters.temperature}, 
                Profundidad {parameters.reasoningDepth}, 
                Estilo {parameters.responseStyle}
              </p>
            </div>
          </div>
        )}

        

        {/* Chat Messages */}
        <div className="bg-slate-800/50 rounded-2xl border border-slate-600/50 backdrop-blur-sm p-6 mb-6 h-96 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <Bot className="h-16 w-16 text-slate-400 mx-auto mb-4" />
                {!modelStatus || modelStatus.status !== 'trained' ? (
                  <>
                    <p className="text-red-400 text-lg font-bold mb-2">
                      ⚠️ Modelo No Disponible
                    </p>
                    <p className="text-slate-400 text-sm mb-4">
                      No hay un modelo entrenado. Entrena un modelo primero.
                    </p>
                    <Link 
                      to="/training"
                      className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-500/20 border border-blue-400/30 rounded-lg text-blue-400 hover:bg-blue-500/30 transition-colors"
                    >
                      <Upload className="h-4 w-4" />
                      <span>Ir a Entrenamiento</span>
                    </Link>
                  </>
                ) : (
                  <>
                    <p className="text-slate-400 text-lg">
                      Haz una pregunta para ver el proceso de razonamiento
                    </p>
                    <p className="text-slate-500 text-sm mt-2">
                      Ejemplo: "¿Por qué no debo echar ácido a un cultivo acuapónico?"
                    </p>
                  </>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex items-start space-x-3 ${
                    message.type === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {message.type !== 'user' && (
                    <div className="flex-shrink-0">
                      {getMessageIcon(message.type)}
                    </div>
                  )}
                  <div
                    className={`max-w-3xl p-4 rounded-2xl border backdrop-blur-sm transition-all duration-300 ${
                      message.type === 'user'
                        ? 'bg-blue-500/20 border-blue-400/30 text-blue-100'
                        : message.isTyping
                        ? `${getMessageStyle(message.type)} animate-pulse border-opacity-60`
                        : getMessageStyle(message.type)
                    }`}
                  >
                    {message.isTyping ? (
                      <div className="flex items-center space-x-3">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                        <div className="flex-1">
                          <div className="text-sm font-medium">Generando respuesta...</div>
                          <div className="text-xs opacity-70">Aplicando razonamiento inteligente</div>
                        </div>
                        <div className="text-xs opacity-50">
                          {message.type === 'system' && 'Iniciando...'}
                          {message.type === 'analysis' && 'Analizando...'}
                          {message.type === 'reasoning' && 'Razonando...'}
                          {message.type === 'base_response' && 'Generando...'}
                          {message.type === 'reasoned_response' && 'Mejorando...'}
                          {message.type === 'patterns' && 'Analizando...'}
                          {message.type === 'final_response' && 'Finalizando...'}
                        </div>
                      </div>
                    ) : (
                      <div className="leading-relaxed">
                        <MarkdownRenderer content={message.content} />
                      </div>
                    )}
                  </div>
                  {message.type === 'user' && (
                    <div className="flex-shrink-0">
                      {getMessageIcon(message.type)}
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
          

        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={
                isProcessing 
                  ? "Procesando tu pregunta..." 
                  : !modelStatus || modelStatus.status !== 'trained' 
                  ? "Entrena un modelo primero..." 
                  : "Escribe tu pregunta aquí..."
              }
              disabled={isProcessing || !modelStatus || modelStatus.status !== 'trained'}
              className={`w-full px-4 py-3 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 backdrop-blur-sm transition-all duration-300 ${
                isProcessing 
                  ? 'bg-orange-900/30 border-orange-500/50 text-orange-100 placeholder-orange-300/50 cursor-not-allowed shadow-lg shadow-orange-500/25' 
                  : !modelStatus || modelStatus.status !== 'trained'
                  ? 'bg-slate-800/50 border-slate-600/50 text-slate-400 placeholder-slate-500 cursor-not-allowed opacity-50'
                  : 'bg-slate-800/50 border-slate-600/50 text-white placeholder-slate-400 focus:ring-purple-500 focus:border-transparent hover:border-slate-500/50'
              }`}
            />
          </div>
          <button
            type="submit"
            disabled={!inputValue.trim() || isProcessing || !modelStatus || modelStatus.status !== 'trained'}
            className={`px-6 py-3 rounded-xl font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 transition-all duration-300 flex items-center space-x-2 ${
              isProcessing 
                ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white cursor-not-allowed opacity-90 shadow-lg shadow-orange-500/25' 
                : !modelStatus || modelStatus.status !== 'trained'
                ? 'bg-gradient-to-r from-gray-500 to-gray-600 text-white cursor-not-allowed opacity-50'
                : 'bg-gradient-to-r from-purple-500 to-blue-500 text-white hover:from-purple-600 hover:to-blue-600 focus:ring-purple-500 shadow-lg shadow-purple-500/25 hover:shadow-xl hover:shadow-purple-500/30'
            }`}
          >
            {isProcessing ? (
              <>
                <div className="relative">
                  <Clock className="h-5 w-5 animate-spin" />
                  <div className="absolute inset-0 rounded-full border-2 border-white/20 border-t-white animate-spin"></div>
                </div>
                <span className="font-semibold">Procesando ({currentStep}/7)</span>
              </>
            ) : !modelStatus || modelStatus.status !== 'trained' ? (
              <>
                <Upload className="h-5 w-5" />
                <span>Entrenar Modelo</span>
              </>
            ) : (
              <>
                <Send className="h-5 w-5" />
                <span>Enviar</span>
              </>
            )}
          </button>
        </form>

        {/* Tips */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-600/50 backdrop-blur-sm">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
              <Brain className="h-5 w-5 text-purple-400" />
              <span>Tipos de Preguntas</span>
            </h3>
            <ul className="text-slate-300 space-y-2 text-sm">
              <li>• <strong>Seguridad:</strong> "¿Por qué no debo usar ácido?"</li>
              <li>• <strong>Causal:</strong> "¿Por qué crecen mejor las plantas?"</li>
              <li>• <strong>Problemas:</strong> "¿Qué hago si los peces están en la superficie?"</li>
              <li>• <strong>Técnico:</strong> "¿Cómo funciona el ciclo del nitrógeno?"</li>
            </ul>
          </div>
          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-600/50 backdrop-blur-sm">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
              <Target className="h-5 w-5 text-green-400" />
              <span>Proceso de Razonamiento</span>
            </h3>
            <ul className="text-slate-300 space-y-2 text-sm">
              <li>1. <strong>Análisis</strong> de la pregunta</li>
              <li>2. <strong>Detección</strong> de contexto</li>
              <li>3. <strong>Razonamiento</strong> aplicado</li>
              <li>4. <strong>Respuesta</strong> mejorada</li>
              <li>5. <strong>Análisis</strong> de patrones</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotReasoning; 