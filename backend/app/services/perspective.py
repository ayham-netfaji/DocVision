import cv2
import numpy as np
from typing import Tuple


class PerspectiveTransformer:
    """
    Performs 4-point perspective transformation (homography) to deskew
    and flatten tilted, rotated, or angled document photos into a flat,
    top-down rectangular scanned document.
    """

    @staticmethod
    def calculate_dimensions(pts: np.ndarray) -> Tuple[int, int]:
        """
        Calculates maximum width and height for target transformed rectangle
        using Euclidean distance between corresponding corner pairs:
        width = max(distance(BR, BL), distance(TR, TL))
        height = max(distance(TR, BR), distance(TL, BL))
        """
        (tl, tr, br, bl) = pts

        # Width calculation
        width_bottom = np.linalg.norm(br - bl)
        width_top = np.linalg.norm(tr - tl)
        max_width = max(int(width_bottom), int(width_top))

        # Height calculation
        height_right = np.linalg.norm(tr - br)
        height_left = np.linalg.norm(tl - bl)
        max_height = max(int(height_right), int(height_left))

        # Safety minimum dimension
        max_width = max(max_width, 10)
        max_height = max(max_height, 10)

        return max_width, max_height

    def four_point_transform(
        self,
        image: np.ndarray,
        pts: np.ndarray,
        scale_ratio: float = 1.0
    ) -> np.ndarray:
        """
        Applies homography transformation to crop and rectify document.
        - image: input image (color or grayscale)
        - pts: 4 corners [TL, TR, BR, BL] detected from resized image
        - scale_ratio: scale factor to map coordinates back if image was downscaled
        """
        scaled_pts = pts.copy()
        if scale_ratio != 1.0 and scale_ratio > 0:
            scaled_pts = scaled_pts / scale_ratio

        max_width, max_height = self.calculate_dimensions(scaled_pts)

        # Destination rectangle points in top-down orientation
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype="float32")

        # Compute perspective transform matrix
        M = cv2.getPerspectiveTransform(scaled_pts.astype("float32"), dst)

        # Apply warp perspective
        warped = cv2.warpPerspective(
            image,
            M,
            (max_width, max_height),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )

        return warped
