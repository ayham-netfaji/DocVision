import numpy as np
import pytest
from app.services.document_processor import DocumentProcessor

@pytest.fixture
def sample_color_image():
    # 2000 x 3000 synthetic color test image
    img = np.zeros((2000, 3000, 3), dtype=np.uint8)
    # Add colored rectangles and variations
    img[200:1800, 300:2700] = [240, 240, 240]  # white page
    img[400:600, 500:2500] = [10, 10, 10]      # text block simulator
    return img

def test_document_processor_resize(sample_color_image):
    processor = DocumentProcessor(max_dimension=1500)
    resized, ratio = processor.resize_image(sample_color_image)

    h, w = resized.shape[:2]
    assert max(h, w) == 1500
    assert ratio == 0.5  # 1500 / 3000
    assert w == 1500
    assert h == 1000

def test_document_processor_small_image_no_upscale():
    processor = DocumentProcessor(max_dimension=1500)
    small_img = np.ones((800, 600, 3), dtype=np.uint8) * 128
    resized, ratio = processor.resize_image(small_img)

    assert ratio == 1.0
    assert resized.shape == small_img.shape

def test_document_processor_grayscale(sample_color_image):
    processor = DocumentProcessor()
    gray = processor.to_grayscale(sample_color_image)

    assert len(gray.shape) == 2
    assert gray.shape == (2000, 3000)
    # Grayscale on already gray should return single channel copy
    gray_again = processor.to_grayscale(gray)
    assert gray_again.shape == gray.shape

def test_document_processor_gaussian_blur(sample_color_image):
    processor = DocumentProcessor()
    gray = processor.to_grayscale(sample_color_image)
    blurred = processor.apply_gaussian_blur(gray, kernel_size=(5, 5))

    assert blurred.shape == gray.shape
    assert blurred.dtype == np.uint8

def test_document_processor_full_pipeline(sample_color_image):
    processor = DocumentProcessor(max_dimension=1200)
    pipeline_result = processor.preprocess_pipeline(sample_color_image)

    assert "resized" in pipeline_result
    assert "ratio" in pipeline_result
    assert "grayscale" in pipeline_result
    assert "blurred" in pipeline_result

    assert max(pipeline_result["resized"].shape[:2]) == 1200
    assert len(pipeline_result["grayscale"].shape) == 2
    assert len(pipeline_result["blurred"].shape) == 2
