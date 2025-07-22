export interface ModelStatus {
  status: 'idle' | 'training' | 'trained' | 'error' | 'not_initialized';
  is_training: boolean;
  progress: number;
  message: string;
  model_stats: {
    patterns_stored?: number;
    memory_kb?: number;
    sparsity?: number;
  };
  model_info?: {
    is_trained: boolean;
    patterns_count: number;
    word_vectors_count: number;
    pattern_graph_nodes: number;
    memory_usage_kb: number;
    max_pattern_length: number;
    min_frequency: number;
    max_patterns: number;
  };
  patterns_stored: number;
  memory_kb: number;
  is_trained?: boolean;
}

export interface UploadedFile {
  filename: string;
  size_bytes: number;
  uploaded_at: string;
}

export interface SavedModel {
  filename: string;
  size_bytes: number;
  created_at: string;
  model_name: string;
}

export interface TrainingResult {
  message: string;
  training_data: {
    files_processed: number;
    lines_processed: number;
    patterns_extracted: number;
    memory_used_kb: number;
  };
  model_stats: {
    patterns_stored: number;
    memory_kb: number;
    sparsity: number;
  };
}

export interface GenerationResult {
  prompt: string;
  generated_text: string;
  base_response?: string;
  reasoned_response?: string;
  parameters: {
    max_length: number;
    temperature: number;
    intelligent_mode?: boolean;
  };
  analysis?: {
    active_patterns: number;
    patterns: Array<{
      pattern: string;
      score: number;
    }>;
  };
  reasoning_analysis?: {
    question_type: string;
    detected_types: string[];
    acuaponia_contexts: string[];
    reasoning_chain: string[];
    active_patterns: number;
    patterns: Array<{
      pattern: string;
      score: number;
    }>;
  };
}

export interface TrainingConfig {
  max_patterns: number;
  max_pattern_length: number;
  min_frequency: number;
}

export interface ModelSaveResult {
  message: string;
  filename: string;
  filepath: string;
  model_info: {
    is_trained: boolean;
    patterns_count: number;
    word_vectors_count: number;
    pattern_graph_nodes: number;
    memory_usage_kb: number;
    max_pattern_length: number;
    min_frequency: number;
    max_patterns: number;
  };
  size_bytes: number;
}

export interface ModelLoadResult {
  message: string;
  filename: string;
  model_info: {
    is_trained: boolean;
    patterns_count: number;
    word_vectors_count: number;
    pattern_graph_nodes: number;
    memory_usage_kb: number;
    max_pattern_length: number;
    min_frequency: number;
    max_patterns: number;
  };
} 