# Site tooling. Python env is managed by uv (deps in requirements.txt).
# Quarto's jupyter engine defaults to system Python, which lacks jupyter — so we
# point it at the uv-managed .venv via QUARTO_PYTHON. Matches CI's Python 3.13.
PY := $(CURDIR)/.venv/bin/python

.PHONY: setup preview preview-all render clean

setup:  ## Create the uv venv (Python 3.13) + install requirements.txt
	uv venv --python 3.13 --allow-existing
	uv pip install --python $(PY) -r requirements.txt

preview:  ## Live full-site preview incl. drafts (uses the venv python)
	QUARTO_PYTHON=$(PY) QUARTO_PROFILE=drafts quarto preview

preview-all:  ## Live full-site preview, published pages only (no drafts)
	QUARTO_PYTHON=$(PY) quarto preview

render:  ## Full-site render to _site/ (uses the venv python)
	QUARTO_PYTHON=$(PY) quarto render

clean:  ## Remove Quarto build output
	rm -rf _site .quarto
