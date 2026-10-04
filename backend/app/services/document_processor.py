import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Union


class DocumentProcessor:
    """
    Core Computer Vision processor implementing fundamental preprocessing
    stages from DocVision Report:
    - Aspect-ratio preserving resizing
    - Grayscale conversion
    - Gaussian blur noise filtration
    """

    def __init__(self, max_dimension: int = 1600):
        self.max_dimension = max_dimension

    def load_image(self, image_source: Union[str, Path, bytes, np.ndarray]) -> np.ndarray:
        """
        Loads an image from file path, raw bytes, or returns existing ndarray.
        Returns BGR numpy image array.
        """
        if isinstance(image_source, np.ndarray):
            return image_source.copy()

        if isinstance(image_source, (str, Path)):
            path_str = str(image_source)
            # Use imdecode to be Windows-safe with unicode paths
            with open(path_str, "rb") as f:
                bytes_data = f.read()
            image_array = np.frombuffer(bytes_data, dtype=np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError(f"Could not decode image at path: {path_str}")
            return img

        if isinstance(image_source, bytes):
            image_array = np.frombuffer(image_source, dtype=np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Could not decode image from provided byte stream.")
            return img

        raise TypeError(f"Unsupported image source type: {type(image_source)}")

    def resize_image(self, image: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Resizes the image if width or height exceeds max_dimension,
        maintaining the original aspect ratio.
        Returns (resized_image, ratio).
        """
        height, width = image.shape[:2]
        max_dim = max(height, width)

        if max_dim <= self.max_dimension:
            return image.copy(), 1.0

        ratio = self.max_dimension / float(max_dim)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized, ratio

    def to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Converts BGR or RGB image to single-channel 8-bit grayscale.
        """
        if len(image.shape) == 2:
            return image.copy()  # Already grayscale

        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def apply_gaussian_blur(self, gray_image: np.ndarray, kernel_size: Tuple[int, int] = (5, 5), sigma_x: float = 0) -> np.ndarray:
        """
        Applies Gaussian blur to smooth high-frequency noise prior to edge detection.
        """
        # Kernel size must be odd and positive
        kx = kernel_size[0] if kernel_size[0] % 2 != 0 else kernel_size[0] + 1
        ky = kernel_size[1] if kernel_size[1] % 2 != 0 else kernel_size[1] + 1
        return cv2.GaussianBlur(gray_image, (kx, ky), sigma_x)

    def preprocess_pipeline(self, image_source: Union[str, Path, bytes, np.ndarray]) -> dict:
        """
        Executes Phase 5 pipeline stages sequentially:
        Original -> Resized -> Grayscale -> Blurred.
        """
        original = self.load_image(image_source)
        resized, ratio = self.resize_image(original)
        gray = self.to_grayscale(resized)
        blurred = self.apply_gaussian_blur(gray)

        return {
            "original_shape": original.shape,
            "resized": resized,
            "ratio": ratio,
            "grayscale": gray,
            "blurred": blurred
        }
