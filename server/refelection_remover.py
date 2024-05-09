from utils import compute_laplacian, normalize_array, double_dct, double_idct
import numpy as np
import matplotlib.pyplot as plt

class ReflectionSuppressor:
    """
    This class processes images to reduce reflections based on the technique described in
    the paper "Fast Single Image Reflection Suppression via Convex Optimization" (https://arxiv.org/pdf/1903.03889.pdf).
    """

    def __init__(self, h_param):
        """
        Initialize the suppression parameters
        Args:
            h_param (float): Controls the strength of the reflection suppression.
        """
        if not (0 <= h_param <= 1):
            raise ValueError("h_param must be within [0, 1]. Recommended values are between 0 and 0.13.")

        self.h = h_param
        self.lambda_val = 0
        self.mu = 1
        self.epsilon = 1e-8

    def double_poisson(self, image): 
        """
        Double Poisson equation solver for image inpainting.
        """
        channels = image.shape[-1]
        laplacians = np.zeros_like(image)
        # L(div(\delta_h(\grad Y)))

        for idx in range(channels):
            temp_lap = compute_laplacian(image[..., idx], h=self.h)
            laplacians[..., idx] = compute_laplacian(temp_lap)

        # Add stability term and scale result
        #  computes right-hand side of equation (7)
        # L(...) + \epsilon * Y
        rhs = laplacians + self.epsilon * image
        return rhs

    def super_supression(self, poisson_result):
        """
        T_{m,n} = F_c^{-1} \left( \frac{F_c(P)_{m,n}}{K_{m,n}^2 + \epsilon} \right)
        """
        T = np.zeros_like(poisson_result)

        # Solve Poisson DCT
        for i in range(poisson_result.shape[-1]):
            current_slice = poisson_result[..., i]
            M, N = current_slice.shape

            # Kappa Matrix |  kappa_{mn} = 2 * [cos((pi * m) / M) + cos((pi * n) / N) - 2]
            kappa = 2 * (np.add.outer(np.cos((np.pi * np.arange(M)) / M), np.cos((np.pi * np.arange(N)) / N)) - 2)

            denominator = self.mu * (kappa ** 2) - self.lambda_val * kappa + self.epsilon

            u = double_dct(current_slice)

            u /= denominator
            T[..., i] = double_idct(u)
        
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

        T = self.super_supression(self.double_poisson(image))
        T = normalize_array(T)

        return T
