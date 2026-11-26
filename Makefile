.DEFAULT_GOAL := help

# --all-extras: sem ele o uv run remove matplotlib e ruff do ambiente
UV := uv run --all-extras
CLI := $(UV) algoritmo-canny

IMAGE ?= resources/valve.png
OUTPUT ?= resources/valve_canny.png
SIGMA ?= 1.4
KERNEL ?=
LOW ?= 40
HIGH ?= 100

KERNEL_ARG = $(if $(KERNEL),-k $(KERNEL),)
ARGS = "$(IMAGE)" -s $(SIGMA) --low $(LOW) --high $(HIGH) $(KERNEL_ARG)

.PHONY: help install install-dev run show test format lint clean

help: ## Lista os comandos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*## "}; {printf "  make %-12s %s\n", $$1, $$2}'

install: ## Instala as dependências de execução
	uv sync

install-dev: ## Instala dependências de visualização e desenvolvimento
	uv sync --extra visualization --extra dev

run: ## Executa o filtro: IMAGE, SIGMA, KERNEL, LOW, HIGH e OUTPUT
	$(CLI) $(ARGS) -o "$(OUTPUT)"

show: ## Salva e exibe as etapas do Canny: IMAGE, SIGMA, KERNEL, LOW e HIGH
	$(CLI) $(ARGS) -o "$(OUTPUT)" --stages --show

format: ## Formata o código
	$(UV) ruff format .

lint: ## Verifica problemas no código
	$(UV) ruff check .

clean: ## Remove arquivos gerados
	rm -f resources/*_canny*
