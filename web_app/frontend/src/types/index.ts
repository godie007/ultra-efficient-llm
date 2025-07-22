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
  patterns_stored: number;
  memory_kb: number;
}

export interface UploadedFile {
  filename: string;
  size_bytes: number;
  uploaded_at: string;
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
  parameters: {
    max_length: number;
    temperature: number;
  };
  analysis: {
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