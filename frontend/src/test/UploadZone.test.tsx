import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { UploadZone } from '../components/UploadZone';

describe('UploadZone Component', () => {
  it('renders upload instructions correctly', () => {
    render(<UploadZone onFileSelect={vi.fn()} />);

    expect(screen.getByText(/drop your document here/i)).toBeInTheDocument();
    expect(screen.getByText(/Supports JPG, PNG, WEBP/i)).toBeInTheDocument();
  });

  it('triggers onFileSelect when a valid image file is uploaded', () => {
    const handleFileSelect = vi.fn();
    render(<UploadZone onFileSelect={handleFileSelect} />);

    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    expect(input).not.toBeNull();

    const file = new File(['mock content'], 'test_scan.png', { type: 'image/png' });
    fireEvent.change(input, { target: { files: [file] } });

    expect(handleFileSelect).toHaveBeenCalledTimes(1);
    expect(handleFileSelect).toHaveBeenCalledWith(file);
  });

  it('shows error message when unsupported file format is uploaded', () => {
    const handleFileSelect = vi.fn();
    render(<UploadZone onFileSelect={handleFileSelect} />);

    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(['mock content'], 'document.pdf', { type: 'application/pdf' });
    fireEvent.change(input, { target: { files: [file] } });

    expect(screen.getByText(/invalid file type/i)).toBeInTheDocument();
    expect(handleFileSelect).not.toHaveBeenCalled();
  });

  it('shows error message when file exceeds 10MB limit', () => {
    const handleFileSelect = vi.fn();
    render(<UploadZone onFileSelect={handleFileSelect} />);

    const input = document.querySelector('input[type="file"]') as HTMLInputElement;
    // 11MB file
    const largeFile = new File([new ArrayBuffer(11 * 1024 * 1024)], 'large.jpg', { type: 'image/jpeg' });
    fireEvent.change(input, { target: { files: [largeFile] } });

    expect(screen.getByText(/file is too large/i)).toBeInTheDocument();
    expect(handleFileSelect).not.toHaveBeenCalled();
  });
});
