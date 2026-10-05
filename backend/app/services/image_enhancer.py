from typing import Literal

import cv2
import numpy as np


class ImageEnhancer:
    """
    Image enhancement service for optimizing document scans prior to OCR:
    - CLAHE (Contrast Limited Adaptive Histogram Equalization) for uneven shadows
    - Adaptive Gaussian & Otsu binarization for clean high-contrast black/white scan
    - Unsharp mask sharpening to restore blurred character edges
    - Configurable enhancement modes: 'scan_bw', 'enhanced_color', 'grayscale'
    """

    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 2:
            return image.copy()
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def apply_clahe(self, gray_image: np.ndarray, clip_limit: float = 2.0, tile_grid_size=(8, 8)) -> np.ndarray:
        """
        Equalizes contrast locally to eliminate shadows and gradients across the page.
        """
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(gray_image)

    def sharpen_image(self, image: np.ndarray, strength: float = 1.5) -> np.ndarray:
        """
        Applies unsharp mask sharpening: sharpened = image * (1 + strength) - blurred * strength
        """
        blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=3)
        sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
        return sharpened

    def adaptive_threshold_bw(self, gray_image: np.ndarray, block_size: int = 15, c_offset: int = 8) -> np.ndarray:
        """
        Applies adaptive Gaussian thresholding to produce crisp black text on pure white paper.
        """
        # Block size must be odd and > 1
        bs = block_size if block_size % 2 != 0 else block_size + 1
        bs = max(3, bs)
        return cv2.adaptiveThreshold(
            gray_image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            bs,
            c_offset
        )

    def otsu_threshold(self, gray_image: np.ndarray) -> np.ndarray:
        """
        Calculates optimal global threshold using Otsu's binarization algorithm.
        """
        # Slight Gaussian blur to reduce single-pixel noise before Otsu
        blurred = cv2.GaussianBlur(gray_image, (3, 3), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def enhance(
        self,
        image: np.ndarray,
        mode: Literal["scan_bw", "enhanced_color", "grayscale"] = "scan_bw"
    ) -> np.ndarray:
        """
        Full enhancement pipeline according to selected mode:
        - 'scan_bw': CLAHE + Sharpen + Adaptive Binarization (Best for OCR)
        - 'enhanced_color': LAB CLAHE on L-channel + Color Sharpen
        - 'grayscale': CLAHE + Grayscale Sharpen
        """
        if mode == "scan_bw":
            gray = self.to_grayscale(image)
            equalized = self.apply_clahe(gray, clip_limit=2.0)
            # Use Gaussian smoothing + Otsu binarization to produce clean solid characters without moire noise
            blurred = cv2.GaussianBlur(equalized, (3, 3), 0)
            _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return binary

        elif mode == "grayscale":
            gray = self.to_grayscale(image)
            equalized = self.apply_clahe(gray, clip_limit=2.0)
            return self.sharpen_image(equalized, strength=1.0)

        elif mode == "enhanced_color":
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            # Enhance luminance in LAB color space
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l_chan, a_chan, b_chan = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l_chan)
            merged = cv2.merge((cl, a_chan, b_chan))
            enhanced_bgr = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
            return self.sharpen_image(enhanced_bgr, strength=0.5)

        raise ValueError(f"Unknown enhancement mode: {mode}")
