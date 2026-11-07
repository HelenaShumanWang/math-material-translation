import os
from pathlib import Path

import pytest

from mathtrans.samples import make_sample_pdf


@pytest.fixture(scope="session")
def samples_dir(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("samples")


@pytest.fixture(scope="session")
def sample_pdf_zh(samples_dir) -> Path:
    return make_sample_pdf(samples_dir / "sample_zh.pdf", "zh")


@pytest.fixture(scope="session")
def sample_pdf_en(samples_dir) -> Path:
    return make_sample_pdf(samples_dir / "sample_en.pdf", "en")


@pytest.fixture
def offline_settings(monkeypatch, tmp_path):
    """Settings pointing at a temp data dir with the offline mock translator."""
    from mathtrans.config import get_settings, reset_settings

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.setenv("MATHTRANS_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("MATHTRANS_TRANSLATOR", "mock")
    monkeypatch.setenv("MATHTRANS_OCR_ENGINE", "rapid")
    reset_settings()
    yield get_settings()
    reset_settings()
