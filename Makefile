.PHONY: install test serve sample demo
install:
	pip install -e ".[dev]"
test:
	python -m pytest -q
serve:
	python -m mathtrans.cli serve --host 0.0.0.0 --port 8000
sample:
	python -m mathtrans.cli sample examples/sample_zh.pdf --lang zh
demo: sample
	python -m mathtrans.cli translate examples/sample_zh.pdf --to en --bilingual --docx --out examples/output/zh_en
