# jonathanwhitmore.com

Personal website and blog built with [Quarto](https://quarto.org/).

## Local Development

```bash
quarto preview
```

To preview posts that use Python kernels, point Quarto at the project venv:

```bash
QUARTO_PYTHON=.venv/bin/python quarto preview
```

Draft posts (`draft: true`) render as empty pages by default, even in preview.
To see them, enable the drafts profile:

```bash
QUARTO_PROFILE=drafts QUARTO_PYTHON=.venv/bin/python quarto preview
```

## License

Content is copyright Jonathan Whitmore. Code is [Apache 2.0](LICENSE).
