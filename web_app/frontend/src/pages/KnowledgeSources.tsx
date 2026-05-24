import { useState, useEffect, useRef } from 'react';
import { Plus, Upload, BookOpen, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { listSources, addSource, updateSource, deleteSource, uploadSources } from '../services/api';
import { Source } from '../types';
import SourceItem from '../components/SourceItem';

const KnowledgeSources: React.FC = () => {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(true);
  const [newText, setNewText] = useState('');
  const [adding, setAdding] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  const load = async () => {
    try {
      const data = await listSources();
      setSources(data.sources);
    } catch {
      toast.error('No pude cargar las fuentes. ¿Está corriendo el backend?');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleAdd = async () => {
    const text = newText.trim();
    if (!text) return;
    setAdding(true);
    try {
      const doc = await addSource(text);
      setSources((prev) => [...prev, doc]);
      setNewText('');
      toast.success('Fuente añadida');
    } catch {
      toast.error('Error al añadir la fuente');
    } finally {
      setAdding(false);
    }
  };

  const handleUpdate = async (id: string, text: string) => {
    try {
      const updated = await updateSource(id, text);
      setSources((prev) => prev.map((s) => (s.id === id ? updated : s)));
      toast.success('Fuente actualizada');
    } catch {
      toast.error('Error al actualizar');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteSource(id);
      setSources((prev) => prev.filter((s) => s.id !== id));
      toast.success('Fuente eliminada');
    } catch {
      toast.error('Error al eliminar');
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      const result = await uploadSources(file);
      toast.success(`${result.added} fuentes añadidas`);
      load();
    } catch {
      toast.error('Error al subir el archivo');
    } finally {
      if (fileInput.current) fileInput.current.value = '';
    }
  };

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gradient flex items-center gap-2">
          <BookOpen className="h-6 w-6 text-blue-400" /> Fuentes de conocimiento
        </h1>
        <div>
          <input
            ref={fileInput}
            type="file"
            accept=".txt,.md,.csv,.json"
            className="hidden"
            onChange={handleUpload}
          />
          <button className="btn-secondary" onClick={() => fileInput.current?.click()}>
            <Upload className="h-4 w-4 inline mr-2" /> Subir archivo
          </button>
        </div>
      </div>

      <div className="card mb-6">
        <h2 className="text-lg font-bold mb-3">Añadir fuente</h2>
        <textarea
          className="input-field resize-none mb-3"
          rows={3}
          placeholder="Escribe un fragmento de conocimiento (un concepto autocontenido)..."
          value={newText}
          onChange={(e) => setNewText(e.target.value)}
        />
        <button className="btn-primary" onClick={handleAdd} disabled={adding || !newText.trim()}>
          {adding ? <Loader2 className="h-4 w-4 animate-spin inline mr-2" /> : <Plus className="h-4 w-4 inline mr-2" />}
          Añadir
        </button>
      </div>

      <h2 className="text-lg font-bold mb-3">Documentos ({sources.length})</h2>

      {loading ? (
        <div className="card-neutral text-center text-slate-300">
          <Loader2 className="h-6 w-6 animate-spin mx-auto text-blue-400" />
        </div>
      ) : sources.length === 0 ? (
        <div className="card-neutral text-center text-slate-300">
          No hay fuentes todavía. Añade una arriba o sube un archivo.
        </div>
      ) : (
        <div className="space-y-3">
          {sources.map((source) => (
            <SourceItem
              key={source.id}
              source={source}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default KnowledgeSources;
