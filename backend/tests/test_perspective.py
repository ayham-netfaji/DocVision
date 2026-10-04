import numpy as np
import cv2
import pytest
from app.services.perspective import PerspectiveTransformer

@pytest.fixture
def angled_document_image():
    # 600 x 600 canvas with a known distorted quad
    img = np.zeros((600, 600, 3), dtype=np.uint8)
    # Angled quad coordinates: TL=(100, 120), TR=(450, 100), BR=(480, 520), BL=(80, 500)
    pts = np.array([[100, 120], [450, 100], [480, 520], [80, 500]], np.int32)
    cv2.fillPoly(img, [pts], (255, 255, 255))
    return img, pts.astype("float32")

def test_calculate_dimensions():
    pts = np.array([
        [0, 0],
        [300, 0],
        [300, 400],
        [0, 400]
    ], dtype="float32")

    transformer = PerspectiveTransformer()
    w, h = transformer.calculate_dimensions(pts)
    assert w == 300
    assert h == 400

def test_four_point_transform_shape(angled_document_image):
    img, pts = angled_document_image
    transformer = PerspectiveTransformer()

    warped = transformer.four_point_transform(img, pts)

    assert warped is not None
    # Result must be a 2D/3D rectangular image
    h, w = warped.shape[:2]
    assert w > 300 and w < 450
    assert h > 350 and h < 450

    # Interior should be uniformly white (since we warped a filled white quad)
    center_pixel = warped[h // 2, w // 2]
    np.testing.assert_array_equal(center_pixel, [255, 255, 255])

def test_four_point_transform_with_scale():
    img = np.ones((1000, 1000, 3), dtype=np.uint8) * 200
    # Coordinates detected on a 0.5 downscaled image (500x500 space)
    downscaled_pts = np.array([
        [50, 50],
        [250, 50],
        [250, 350],
        [50, 350]
    ], dtype="float32")

    transformer = PerspectiveTransformer()
    # Passing scale_ratio=0.5 will scale coordinates back up to full 1000x1000 image
    warped = transformer.four_point_transform(img, downscaled_pts, scale_ratio=0.5)

    h, w = warped.shape[:2]
    assert w == 400  # (250-50) * 2
    assert h == 600  # (350-50) * 2
