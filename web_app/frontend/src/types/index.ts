export interface Source {
  id: string;
  text: string;
}

export interface SourceRef {
  id: string | null;
  text: string;
  score: number;
}

export interface ChatResponse {
  answer: string;
  sources: SourceRef[];
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceRef[];
}

export interface Health {
  status: string;
  model: string;
  instruct: boolean;
  device: string;
  num_sources: number;
}
