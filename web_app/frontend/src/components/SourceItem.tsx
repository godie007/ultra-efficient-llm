import { useState } from 'react';
import { Trash2, Pencil, Check, X } from 'lucide-react';
import { Source } from '../types';

interface Props {
  source: Source;
  onUpdate: (id: string, text: string) => Promise<void> | void;
  onDelete: (id: string) => Promise<void> | void;
}

const SourceItem: React.FC<Props> = ({ source, onUpdate, onDelete }) => {
  const [editing, setEditing] = useState(false);
  const [text, setText] = useState(source.text);

  const save = async () => {
    if (!text.trim()) return;
    await onUpdate(source.id, text.trim());
    setEditing(false);
  };

  const cancel = () => {
    setText(source.text);
    setEditing(false);
  };

  return (
    <div className="card-neutral !p-4">
      {editing ? (
        <div>
          <textarea
            className="input-field resize-none mb-3"
            rows={3}
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <div className="flex gap-2">
            <button className="btn-success" onClick={save}>
              <Check className="h-4 w-4 inline mr-1" /> Guardar
            </button>
            <button className="btn-secondary" onClick={cancel}>
              <X className="h-4 w-4 inline mr-1" /> Cancelar
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1">
            <span className="badge badge-neutral mb-2">{source.id}</span>
            <p className="text-slate-200 text-sm">{source.text}</p>
          </div>
          <div className="flex gap-2 shrink-0">
            <button className="btn-secondary !py-2 !px-3" onClick={() => setEditing(true)}>
              <Pencil className="h-4 w-4" />
            </button>
            <button className="btn-danger" onClick={() => onDelete(source.id)}>
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SourceItem;
