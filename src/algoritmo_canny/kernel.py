import numpy as np


def gaussian_kernel_1d(
    sigma: float,
    size: int | None = None,
) -> np.ndarray:
    """
    Gera um kernel gaussiano 1D normalizado.

    Args:
        sigma (float): Desvio padrão da função gaussiana.
        size (int | None): Tamanho do kernel. Se None, será calculado automaticamente.
    Returns:
        np.ndarray: Kernel gaussiano 1D normalizado.
    """
    if sigma <= 0:
        raise ValueError("sigma must be greater than zero")

    if size is None:
        size = int(2 * np.ceil(3 * sigma) + 1)

    if size <= 0:
        raise ValueError("size must be greater than zero")

    if size % 2 == 0:
        size += 1

    radius = size // 2
    x = np.arange(-radius, radius + 1, dtype=np.float64)
    kernel = np.exp(-(x**2) / (2 * sigma**2))

    return kernel / kernel.sum()
