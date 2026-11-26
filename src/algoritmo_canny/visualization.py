import numpy as np

from algoritmo_canny.canny import CannyStages


def show_stages(original: np.ndarray, stages: CannyStages) -> None:
    """
    Exibe a imagem original e cada etapa do Canny em um grid 2x3.

    Args:
        original (np.ndarray): A imagem original em tons de cinza.
        stages (CannyStages): Resultado de cada etapa do Canny.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib não instalado (make install-dev); exibição ignorada.")
        return

    images = [original, *stages]
    titles = [
        "Original",
        "Suavizada (gaussiana)",
        "Magnitude (Sobel)",
        "Afinada (NMS)",
        "Limiar duplo",
        "Bordas (histerese)",
    ]
    _, axes = plt.subplots(2, 3, figsize=(12, 8))

    for ax, image, title in zip(axes.flat, images, titles):
        ax.imshow(image, cmap="gray")
        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()
    plt.show()
