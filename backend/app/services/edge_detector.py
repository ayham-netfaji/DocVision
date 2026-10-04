
import cv2
import numpy as np


class EdgeDetector:
    """
    OpenCV document edge and contour detector:
    - Auto/adaptive Canny edge detection
    - Morphological closing/dilation to connect broken lines
    - Contour ranking by area
    - Polygon approximation to extract 4-point quadrilateral
    - Consistent point ordering (TL, TR, BR, BL)
    - Fallback mechanism to full bounding box if document edges not found
    """

    def __init__(self, min_area_ratio: float = 0.05):
        self.min_area_ratio = min_area_ratio

    def auto_canny(self, image: np.ndarray, sigma: float = 0.33) -> np.ndarray:
        """
        Computes automatic Canny thresholds based on median pixel intensity.
        """
        v = np.median(image)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        return cv2.Canny(image, lower, upper)

    def detect_edges(self, gray_blurred: np.ndarray) -> np.ndarray:
        """
        Runs edge detection followed by morphological dilation and closing
        to solidify boundary lines.
        """
        edges = self.auto_canny(gray_blurred)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        dilated = cv2.dilate(closed_edges, kernel, iterations=1)
        return dilated

    def order_points(self, pts: np.ndarray) -> np.ndarray:
        """
        Orders coordinates: [top-left, top-right, bottom-right, bottom-left].
        pts: shape (4, 2)
        """
        rect = np.zeros((4, 2), dtype="float32")

        # Sum: top-left has smallest sum, bottom-right has largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # Difference: top-right has smallest diff (x - y), bottom-left largest diff
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def find_document_contour(self, edge_image: np.ndarray, original_shape: tuple[int, ...]) -> tuple[np.ndarray, bool]:
        """
        Finds the largest 4-sided contour corresponding to the document boundary.
        Returns (ordered_4_corners, is_detected).
        If no qualified 4-point polygon found, returns full image corners as fallback.
        """
        contours, _ = cv2.findContours(edge_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        h, w = original_shape[:2]
        min_area = (h * w) * self.min_area_ratio

        for c in contours[:5]:
            area = cv2.contourArea(c)
            if area < min_area:
                continue

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # If contour has 4 points and is convex, it's our document
            if len(approx) == 4 and cv2.isContourConvex(approx):
                corners = approx.reshape(4, 2)
                return self.order_points(corners.astype("float32")), True

        # Fallback: full image boundary corners
        fallback_corners = np.array([
            [0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]
        ], dtype="float32")

        return fallback_corners, False
