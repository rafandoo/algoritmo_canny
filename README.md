# <h1 align="center">🔍 Algoritmo de Canny</h1>

> Status do projeto: ✔ Finalizado

## 📝 Descrição do projeto

<p align="justify">
Este projeto demonstra a implementação manual do detector de bordas de Canny no processamento digital de imagens, utilizando Python e NumPy. O algoritmo identifica bordas finas e contínuas, separando contornos reais de variações causadas por ruído.
</p>

## 🤔 Definição do Problema

<p align="justify">
O objetivo do projeto é detectar as bordas de uma imagem digital em tons de cinza seguindo as cinco etapas clássicas do Canny:
</p>

1. **Suavização gaussiana**: reduz o ruído antes de derivar a imagem.
2. **Gradiente (Sobel)**: calcula a magnitude e a direção da variação de intensidade.
3. **Supressão de não máximos**: afina as bordas, mantendo apenas os máximos locais na direção do gradiente.
4. **Limiar duplo**: classifica os pixels em fortes, fracos ou descartados.
5. **Histerese**: mantém os pixels fracos apenas quando estão conectados a um pixel forte.

## 👨‍💻 Tecnologias

<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Logo Python"/>
    <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="Logo NumPy"/>
</p>

## 🔑 Licença

The [MIT License](LICENSE) (MIT)

Copyright © 2026 - Rafael Camargo
