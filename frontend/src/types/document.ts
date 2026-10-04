export interface ProcessingStagePreview {
  id: string;
  name: string;
  description: string;
  image_url: string;
}

export interface ProcessedDocument {
  document_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  original_image_url: string;
  processed_image_url?: string;
  text: string;
  confidence: number;
  word_count?: number;
  character_count?: number;
  created_at?: string;
  stages?: ProcessingStagePreview[];
}

export interface ProcessingStep {
  id: string;
  label: string;
  status: 'pending' | 'current' | 'completed' | 'error';
}
