import { useState } from 'react';
import { Send, Copy, RotateCcw, MessageSquare, Settings, Lightbulb, BarChart3, Zap } from 'lucide-react';
import toast from 'react-hot-toast';
import { generateText } from '../services/api';
import { GenerationResult } from '../types';

const Generation: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [maxLength, setMaxLength] = useState(20);
  const [temperature, setTemperature] = useState(0.7);
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState<GenerationResult | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Ingresa un prompt para generar texto');
      return;
    }

    setGenerating(true);
    try {
      const response = await generateText(prompt, maxLength, temperature);
      setResult(response);
      toast.success('Texto generado exitosamente');
    } catch (error) {
      toast.error('Error al generar texto');
    } finally {
      setGenerating(false);
    }
  };

  const handleCopy = () => {
    if (result) {
      navigator.clipboard.writeText(result.generated_text);
      toast.success('Texto copiado al portapapeles');
    }
  };

  const handleReset = () => {
    setPrompt('');
    setMaxLength(20);
    setTemperature(0.7);
    setResult(null);
  };

  return (
    <div className="space-y-8 p-6 min-h-screen">
      {/* Header con glassmorphism */}
      <div className="relative overflow-hidden rounded-3xl p-8 shadow-3xl">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-600/20 via-teal-600/20 to-cyan-600/20 backdrop-blur-xl"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/80 to-slate-800/80"></div>
        <div className="relative z-10 text-center">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 rounded-2xl backdrop-blur-md border border-emerald-400/30">
              <MessageSquare className="h-16 w-16 text-emerald-400" />
            </div>
          </div>
          <h1 className="text-5xl font-bold mb-4 text-gradient-accent text-shadow">
            Generación de Texto
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Prueba el modelo entrenado con prompts personalizados
          </p>
          <div className="mt-6 flex justify-center">
            <div className="flex items-center space-x-2 bg-slate-800/50 px-4 py-2 rounded-full backdrop-blur-sm border border-slate-600/50">
              <Zap className="h-4 w-4 text-emerald-400" />
              <span className="text-slate-300 text-sm">IA Generativa Avanzada</span>
            </div>
          </div>
        </div>
      </div>

      {/* Input Section con glassmorphism */}
      <div className="card hover-lift">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-2 bg-emerald-500/20 rounded-lg backdrop-blur-sm border border-emerald-400/30">
            <Settings className="h-8 w-8 text-emerald-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">Configuración de Generación</h2>
        </div>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-bold text-slate-300 mb-3">
              Prompt
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Escribe tu prompt aquí..."
              className="input-field h-32 resize-none"
              rows={4}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-slate-300 mb-3">
                Longitud Máxima: {maxLength}
              </label>
              <input
                type="range"
                min="5"
                max="50"
                value={maxLength}
                onChange={(e) => setMaxLength(parseInt(e.target.value))}
                className="w-full h-3 bg-slate-700 rounded-lg appearance-none cursor-pointer slider-custom"
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-300 mb-3">
                Temperatura: {temperature}
              </label>
              <input
                type="range"
                min="0.1"
                max="2.0"
                step="0.1"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                className="w-full h-3 bg-slate-700 rounded-lg appearance-none cursor-pointer slider-custom"
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-6">
            <button
              onClick={handleReset}
              className="btn-secondary flex items-center space-x-2"
            >
              <RotateCcw className="h-4 w-4" />
              <span>Reiniciar</span>
            </button>
            <button
              onClick={handleGenerate}
              disabled={!prompt.trim() || generating}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-3 text-lg"
            >
              {generating ? (
                <>
                  <div className="loading-spinner"></div>
                  <span>Generando...</span>
                </>
              ) : (
                <>
                  <Send className="h-5 w-5" />
                  <span>Generar Texto</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Generated Text */}
          <div className="card card-highlight hover-lift">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-4">
                <div className="p-2 bg-blue-500/20 rounded-lg backdrop-blur-sm border border-blue-400/30">
                  <MessageSquare className="h-6 w-6 text-blue-400" />
                </div>
                <h2 className="text-2xl font-bold text-blue-100">Texto Generado</h2>
              </div>
              <button
                onClick={handleCopy}
                className="btn-secondary flex items-center space-x-2"
              >
                <Copy className="h-4 w-4" />
                <span>Copiar</span>
              </button>
            </div>
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-600/50 backdrop-blur-sm">
              <p className="text-slate-100 whitespace-pre-wrap leading-relaxed">{result.generated_text}</p>
            </div>
          </div>

          {/* Analysis */}
          <div className="card hover-lift">
            <div className="flex items-center space-x-4 mb-6">
              <div className="p-2 bg-purple-500/20 rounded-lg backdrop-blur-sm border border-purple-400/30">
                <BarChart3 className="h-8 w-8 text-purple-400" />
              </div>
              <h2 className="text-2xl font-bold text-white">Análisis</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
                <h3 className="font-bold text-white mb-4">Parámetros Utilizados</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-slate-300">Prompt:</span>
                    <span className="font-medium text-white">{result.prompt}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-300">Longitud Máxima:</span>
                    <span className="font-medium text-emerald-400">{result.parameters.max_length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-300">Temperatura:</span>
                    <span className="font-medium text-blue-400">{result.parameters.temperature}</span>
                  </div>
                </div>
              </div>
              <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
                <h3 className="font-bold text-white mb-4">Patrones Activos</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-slate-300">Total de Patrones:</span>
                    <span className="font-medium text-purple-400">{result.analysis.active_patterns}</span>
                  </div>
                  {result.analysis.patterns.length > 0 && (
                    <div>
                      <span className="text-slate-300 block mb-3">Patrones Principales:</span>
                      <div className="space-y-2">
                        {result.analysis.patterns.map((pattern, index) => (
                          <div key={index} className="flex justify-between text-sm p-2 bg-slate-700/50 rounded-lg">
                            <span className="text-slate-300">{pattern.pattern}</span>
                            <span className="font-medium text-amber-400">{pattern.score.toFixed(3)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tips con glassmorphism */}
      <div className="card hover-lift">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-2 bg-amber-500/20 rounded-lg backdrop-blur-sm border border-amber-400/30">
            <Lightbulb className="h-8 w-8 text-amber-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">Consejos para Mejores Resultados</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
            <h3 className="font-bold text-amber-100 mb-4">Temperatura</h3>
            <ul className="text-sm text-slate-300 space-y-2">
              <li className="flex items-start space-x-2">
                <span className="text-amber-400 mt-1">•</span>
                <div>
                  <strong className="text-amber-100">0.1-0.5:</strong> Respuestas más deterministas
                </div>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-amber-400 mt-1">•</span>
                <div>
                  <strong className="text-amber-100">0.5-1.0:</strong> Balance entre creatividad y coherencia
                </div>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-amber-400 mt-1">•</span>
                <div>
                  <strong className="text-amber-100">1.0-2.0:</strong> Respuestas más creativas y variadas
                </div>
              </li>
            </ul>
          </div>
          <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-600/50 backdrop-blur-sm">
            <h3 className="font-bold text-emerald-100 mb-4">Longitud</h3>
            <ul className="text-sm text-slate-300 space-y-2">
              <li className="flex items-start space-x-2">
                <span className="text-emerald-400 mt-1">•</span>
                <div>
                  <strong className="text-emerald-100">5-10:</strong> Respuestas cortas y directas
                </div>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-emerald-400 mt-1">•</span>
                <div>
                  <strong className="text-emerald-100">10-20:</strong> Respuestas de longitud media
                </div>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-emerald-400 mt-1">•</span>
                <div>
                  <strong className="text-emerald-100">20-50:</strong> Respuestas más elaboradas
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Generation; 