export interface ProcessedDocument {
  document_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  original_image: string;
  processed_image?: string;
  text?: string;
  confidence?: number;
  created_at?: string;
}

export interface ProcessingStep {
  id: string;
  label: string;
  status: 'pending' | 'current' | 'completed' | 'error';
}
