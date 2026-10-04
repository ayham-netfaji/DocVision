import cv2
import numpy as np
import pytest

from app.services.edge_detector import EdgeDetector


@pytest.fixture
def document_image_fixture():
    # 800 x 800 black background with a clean white rectangular document in the center
    img = np.zeros((800, 800), dtype=np.uint8)
    # Draw white quad: [100, 150], [650, 120], [700, 680], [120, 710]
    pts = np.array([[100, 150], [650, 120], [700, 680], [120, 710]], np.int32)
    cv2.fillPoly(img, [pts], 255)
    return img

def test_order_points():
    detector = EdgeDetector()
    unordered = np.array([
        [700, 680],  # BR
        [100, 150],  # TL
        [120, 710],  # BL
        [650, 120]   # TR
    ], dtype="float32")

    ordered = detector.order_points(unordered)

    # Ordered must be [TL, TR, BR, BL]
    np.testing.assert_array_almost_equal(ordered[0], [100, 150])  # TL
    np.testing.assert_array_almost_equal(ordered[1], [650, 120])  # TR
    np.testing.assert_array_almost_equal(ordered[2], [700, 680])  # BR
    np.testing.assert_array_almost_equal(ordered[3], [120, 710])  # BL

def test_edge_detection_and_document_found(document_image_fixture):
    detector = EdgeDetector()
    edges = detector.detect_edges(document_image_fixture)

    assert edges is not None
    assert edges.shape == (800, 800)

    corners, is_detected = detector.find_document_contour(edges, (800, 800))
    assert is_detected is True
    assert corners.shape == (4, 2)

    # Check corners roughly match input polygon coordinates
    assert abs(corners[0][0] - 100) < 15
    assert abs(corners[0][1] - 150) < 15

def test_document_detection_fallback():
    # Plain black image with no contours
    blank = np.zeros((500, 400), dtype=np.uint8)
    detector = EdgeDetector()
    edges = detector.detect_edges(blank)

    corners, is_detected = detector.find_document_contour(edges, (500, 400))
    assert is_detected is False  # Fallback triggered
    assert corners.shape == (4, 2)
    # Check fallback points are full image bounds: (0,0), (399,0), (399,499), (0,499)
    assert corners[0][0] == 0 and corners[0][1] == 0
    assert corners[2][0] == 399 and corners[2][1] == 499
