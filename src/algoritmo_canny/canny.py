from typing import NamedTuple

import numpy as np

from algoritmo_canny.convolution import convolve_1d
from algoritmo_canny.kernel import gaussian_kernel_1d

STRONG = 255
WEAK = 75


class CannyStages(NamedTuple):
    smoothed: np.ndarray
    magnitude: np.ndarray
    thinned: np.ndarray
    classified: np.ndarray
    edges: np.ndarray


def smooth(image: np.ndarray, sigma: float, size: int | None = None) -> np.ndarray:
    """Suavização gaussiana em float, para não arredondar antes do gradiente."""
    kernel = gaussian_kernel_1d(sigma, size)
    result = convolve_1d(image.astype(np.float64), kernel, axis=1)
    return convolve_1d(result, kernel, axis=0)


def sobel(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Calcula magnitude e direção do gradiente com Sobel separável."""
    derivative = np.array([-1.0, 0.0, 1.0])
    average = np.array([1.0, 2.0, 1.0])

    gx = convolve_1d(convolve_1d(image, derivative, axis=1), average, axis=0)
    gy = convolve_1d(convolve_1d(image, derivative, axis=0), average, axis=1)
    return np.hypot(gx, gy), np.arctan2(gy, gx)


def non_maximum_suppression(mag: np.ndarray, angle: np.ndarray) -> np.ndarray:
    """Mantém só os máximos locais na direção do gradiente."""
    p = np.pad(mag, 1)
    sector = np.round(np.rad2deg(angle) % 180 / 45).astype(int) % 4
    # (linha, coluna) do vizinho em 0°, 45°, 90° e 135°; y cresce para baixo
    offsets = [(0, 1), (1, 1), (1, 0), (1, -1)]
    h, w = mag.shape
    keep = np.zeros(mag.shape, dtype=bool)

    for k, (dy, dx) in enumerate(offsets):
        ahead = p[1 + dy : 1 + dy + h, 1 + dx : 1 + dx + w]
        behind = p[1 - dy : 1 - dy + h, 1 - dx : 1 - dx + w]
        # > de um lado e >= do outro: um platô de 2 pixels gera uma só borda
        keep |= (sector == k) & (mag > behind) & (mag >= ahead)

    return np.where(keep, mag, 0.0)


def double_threshold(thin: np.ndarray, low: float, high: float) -> np.ndarray:
    """Classifica pixels em fortes, fracos ou descartados."""
    result = np.zeros(thin.shape, dtype=np.uint8)
    result[(thin >= low) & (thin > 0)] = WEAK
    result[(thin >= high) & (thin > 0)] = STRONG
    return result


def hysteresis(classified: np.ndarray) -> np.ndarray:
    """Mantém pixels fracos só quando ligados (8-vizinhos) a um forte."""
    edges = np.where(classified == STRONG, STRONG, 0).astype(np.uint8)
    h, w = classified.shape
    stack = list(zip(*np.nonzero(edges)))

    while stack:
        y, x = stack.pop()
        for ny in range(max(y - 1, 0), min(y + 2, h)):
            for nx in range(max(x - 1, 0), min(x + 2, w)):
                if classified[ny, nx] == WEAK and not edges[ny, nx]:
                    edges[ny, nx] = STRONG
                    stack.append((ny, nx))

    return edges


def canny(
    image: np.ndarray,
    sigma: float = 1.4,
    low: float = 40.0,
    high: float = 100.0,
    size: int | None = None,
) -> CannyStages:
    """
    Detector de bordas de Canny para imagem 2D em tons de cinza (0 a 255).

    Args:
        image (np.ndarray): Imagem 2D.
        sigma (float): Desvio padrão da suavização gaussiana.
        low (float): Limiar baixo, na escala da magnitude de Sobel.
        high (float): Limiar alto, na escala da magnitude de Sobel.
        size (int | None): Tamanho do kernel. Se None, calculado a partir de sigma.
    Returns:
        CannyStages: Resultado de cada etapa; `edges` é a saída final.
    """
    if image.ndim != 2:
        raise ValueError("image must be grayscale (2D)")
    if not 0 <= low <= high:
        raise ValueError("thresholds must satisfy 0 <= low <= high")

    smoothed = smooth(image, sigma, size)
    magnitude, angle = sobel(smoothed)
    thinned = non_maximum_suppression(magnitude, angle)
    classified = double_threshold(thinned, low, high)
    return CannyStages(
        smoothed, magnitude, thinned, classified, hysteresis(classified)
    )
