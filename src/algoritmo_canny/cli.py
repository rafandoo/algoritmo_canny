import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from algoritmo_canny.canny import canny
from algoritmo_canny.visualization import show_stages


def main() -> None:
    parser = argparse.ArgumentParser(description="Detecta bordas com Canny.")
    parser.add_argument("input", type=Path, help="imagem de entrada")
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("-s", "--sigma", type=float, default=1.4)
    parser.add_argument("-k", "--kernel-size", type=int, default=None)
    parser.add_argument("--low", type=float, default=40.0)
    parser.add_argument("--high", type=float, default=100.0)
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--stages", action="store_true", help="salva cada etapa")
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Arquivo não encontrado: {args.input}")

    with Image.open(args.input) as img:
        gray = np.array(img.convert("L"))

    result = canny(gray, args.sigma, args.low, args.high, args.kernel_size)
    output = args.output or args.input.with_name(f"{args.input.stem}_canny.png")
    Image.fromarray(result.edges).save(output)
    print(f"Imagem salva em: {output}")

    if args.stages:
        # edges (último campo) já foi salva acima como a saída principal
        stages = list(result._asdict().items())[:-1]
        for step, (name, stage) in enumerate(stages, start=1):
            # dividir antes evita overflow em uint8; magnitude passa de 255
            stage = stage / max(stage.max(), 1e-9) * 255
            path = output.with_name(f"{output.stem}_{step}_{name}.png")
            Image.fromarray(stage.astype(np.uint8)).save(path)
            print(f"Etapa salva em: {path}")

    if args.show:
        show_stages(gray, result)


if __name__ == "__main__":
    main()
