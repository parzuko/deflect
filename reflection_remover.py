from utils import dct2, idct2, laplacian
from data_store import DataStorage, normalize_array
import numpy as np
import matplotlib.pyplot as plt

class ReflectionSuppressor:
    """
    This class processes images to reduce reflections based on the technique described in
    the paper "Fast Single Image Reflection Suppression via Convex Optimization" (https://arxiv.org/pdf/1903.03889.pdf).
    """

    def __init__(self, h_param: float, lambda_val: float = 0, mu_val: float = 1, epsilon_val: float = 1e-8, storage: DataStorage = None):
        """
        Initialize the suppression parameters and storage handler for debugging outputs.

        Args:
            h_param (float): Controls the strength of the reflection suppression.
            lambda_val (float, optional): Regularization parameter, default is 0.
            mu_val (float, optional): Weighing parameter, default is 1.
            epsilon_val (float, optional): Stabilization parameter, default is 1e-8.
            storage (DataStorage, optional): If provided, used to save debugging images.
        """
        if not (0 <= h_param <= 1):
            raise ValueError("h_param must be within [0, 1]. Recommended values are between 0 and 0.13.")
        if not (0 <= lambda_val <= 1):
            raise ValueError("lambda_val must be within [0, 1].")
        if not (0 <= mu_val <= 1):
            raise ValueError("mu_val must be within [0, 1].")

        self.h = h_param
        self.lambda_val = lambda_val
        self.epsilon = epsilon_val
        self.mu = mu_val
        self.storage = storage

    def compute_rhs(self, image: np.ndarray) -> np.ndarray:
        """
        Calculate the right-hand side of equation (7) from the paper.
        Args:
            image (np.ndarray): Input image normalized to [0, 1].
        Returns:
            np.ndarray: Computed right-hand side matrix.
        """
        channels = image.shape[-1]
        laplacians = np.zeros_like(image)
        for idx in range(channels):
            temp_lap = laplacian(image[..., idx], h=self.h)
            laplacians[..., idx] = laplacian(temp_lap)

            if self.storage:
                plt.imshow(temp_lap, cmap='gray')
                self.storage.store_figure(temp_lap, filename=f"channel_{idx}_laplacian", group="debug")

        # Add stability term and scale result
        rhs = laplacians + self.epsilon * image
        normalized_rhs = np.interp(rhs, (rhs.min(), rhs.max()), (0, 1))

        if self.storage:
            self.storage.store_figure(normalized_rhs, filename="rhs_normalized", group="debug")

        return rhs

    def compute_T(self, rhs: np.ndarray) -> np.ndarray:
        """
        Solve the equation system to obtain the reflection-suppressed image.
        Args:
            rhs (np.ndarray): Right-hand side computed from the original image.
        Returns:
            np.ndarray: Suppressed image.
        """
        T = np.zeros_like(rhs)
        for c in range(rhs.shape[-1]):
            rhs_slice = rhs[..., c]
            M, N = rhs_slice.shape
            kappa = 2 * (np.add.outer(np.cos((np.pi * np.arange(M)) / M), np.cos((np.pi * np.arange(N)) / N)) - 2)
            denom = self.mu * (kappa ** 2) - self.lambda_val * kappa + self.epsilon
            u = dct2(rhs_slice)
            u /= denom
            T[..., c] = idct2(u)

            if self.storage:
                self.storage.store_figure(T[..., c], filename=f"channel_{c}_T_matrix", group="result")

        return T

    def remove_reflections(self, image: np.ndarray) -> np.ndarray:
        """
        Public method to process an image and suppress reflections.
        Args:
            image (np.ndarray): Original image to be processed, expected to have values between [0, 1].
        Returns:
            np.ndarray: Processed image with reflections suppressed.
        """
        if image.min() < 0 or image.max() > 1:
            raise ValueError("Image must have all values normalized between 0 and 1.")
        if image.ndim != 3:
            raise ValueError("Image must have three dimensions (H, W, C).")

        T = self.compute_T(self.compute_rhs(image))
        normalize_array(T)

        if self.storage:
            self.storage.store_figure(T, filename="final_output", group="result")

        return T
