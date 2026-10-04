import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProcessingStatus } from '../components/ProcessingStatus';
import type { ProcessingStep } from '../types/document';

const mockSteps: ProcessingStep[] = [
  { id: 'upload', label: 'Uploading file', status: 'pending' },
  { id: 'detect', label: 'Detecting boundaries', status: 'pending' },
  { id: 'perspective', label: 'Warping perspective', status: 'pending' },
  { id: 'ocr', label: 'Extracting text via OCR', status: 'pending' },
];

describe('ProcessingStatus Component', () => {
  it('renders all pipeline step labels', () => {
    render(<ProcessingStatus steps={mockSteps} currentStepIndex={1} />);

    expect(screen.getByText('Uploading file')).toBeInTheDocument();
    expect(screen.getByText('Detecting boundaries')).toBeInTheDocument();
    expect(screen.getByText('Warping perspective')).toBeInTheDocument();
    expect(screen.getByText('Extracting text via OCR')).toBeInTheDocument();
  });

  it('calculates and displays progress percentage accurately', () => {
    // Step index 1 out of 4 steps = (1 + 1) / 4 * 100 = 50%
    render(<ProcessingStatus steps={mockSteps} currentStepIndex={1} />);
    expect(screen.getByText('50%')).toBeInTheDocument();

    // Step index 3 out of 4 steps = (3 + 1) / 4 * 100 = 100%
    render(<ProcessingStatus steps={mockSteps} currentStepIndex={3} />);
    expect(screen.getByText('100%')).toBeInTheDocument();
  });
});
