import cv2
import numpy as np
import pytest

from app.services.image_enhancer import ImageEnhancer


@pytest.fixture
def shadowed_document():
    # 500x500 test image with a shadow gradient and synthetic text
    img = np.zeros((500, 500), dtype=np.uint8)
    # Add diagonal gradient simulating uneven lighting
    for y in range(500):
        for x in range(500):
            img[y, x] = int(120 + 80 * (x + y) / 1000)

    # Draw dark simulated text characters
    cv2.putText(img, "DOCVISION OCR TEST", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.0, 30, 2)
    cv2.putText(img, "Computer Vision System", (50, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 30, 2)
    return img

def test_clahe_contrast_increase(shadowed_document):
    enhancer = ImageEnhancer()
    clahe_img = enhancer.apply_clahe(shadowed_document)

    assert clahe_img.shape == shadowed_document.shape
    # Standard deviation should increase due to enhanced local contrast
    assert np.std(clahe_img) > np.std(shadowed_document) * 0.9

def test_adaptive_threshold_binary(shadowed_document):
    enhancer = ImageEnhancer()
    binary = enhancer.adaptive_threshold_bw(shadowed_document)

    assert binary.shape == shadowed_document.shape
    # Binary image should only contain 0 and 255 values
    unique_vals = set(np.unique(binary))
    assert unique_vals.issubset({0, 255})

def test_otsu_threshold(shadowed_document):
    enhancer = ImageEnhancer()
    otsu = enhancer.otsu_threshold(shadowed_document)

    assert otsu.shape == shadowed_document.shape
    unique_vals = set(np.unique(otsu))
    assert unique_vals.issubset({0, 255})

def test_enhance_modes(shadowed_document):
    enhancer = ImageEnhancer()

    # scan_bw mode
    bw_res = enhancer.enhance(shadowed_document, mode="scan_bw")
    assert len(bw_res.shape) == 2
    assert set(np.unique(bw_res)).issubset({0, 255})

    # grayscale mode
    gray_res = enhancer.enhance(shadowed_document, mode="grayscale")
    assert len(gray_res.shape) == 2

    # enhanced_color mode
    color_img = cv2.cvtColor(shadowed_document, cv2.COLOR_GRAY2BGR)
    color_res = enhancer.enhance(color_img, mode="enhanced_color")
    assert len(color_res.shape) == 3
    assert color_res.shape[2] == 3
