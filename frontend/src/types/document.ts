export interface ProcessedDocument {
  document_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  original_image_url: string;
  processed_image_url?: string;
  text: string;
  confidence: number;
  created_at?: string;
}

export interface ProcessingStep {
  id: string;
  label: string;
  status: 'pending' | 'current' | 'completed' | 'error';
}
