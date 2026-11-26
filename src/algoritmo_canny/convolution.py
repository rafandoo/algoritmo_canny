import numpy as np


def convolve_1d(channel: np.ndarray, kernel: np.ndarray, axis: int) -> np.ndarray:
    """Filtro 1D ao longo de um eixo, com borda refletida (do filtro_gaussiano)."""
    radius = len(kernel) // 2
    pad_width = [(0, 0)] * channel.ndim
    pad_width[axis] = (radius, radius)

    padded = np.pad(channel, pad_width, mode="reflect")
    output = np.zeros_like(channel, dtype=np.float64)
    n = channel.shape[axis]

    for i, weight in enumerate(kernel):
        window = [slice(None)] * channel.ndim
        window[axis] = slice(i, i + n)
        output += weight * padded[tuple(window)]

    return output
