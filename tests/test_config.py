from __future__ import annotations

from pathlib import Path

import pytest

from youtube_downloader_skill.config import DownloadConfig, default_output_dir, validate_youtube_url
from youtube_downloader_skill.errors import InvalidURLError


def test_default_output_dir_uses_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert default_output_dir() == tmp_path / "Outputs"


def test_from_inputs_creates_default_outputs_folder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    cfg = DownloadConfig.from_inputs("https://youtu.be/8CcP8hbZpew")

    assert cfg.output_dir == (tmp_path / "Outputs")
    assert cfg.output_dir.exists()


def test_from_inputs_uses_custom_output_folder(tmp_path: Path) -> None:
    custom_dir = tmp_path / "my-target"
    cfg = DownloadConfig.from_inputs("https://youtu.be/8CcP8hbZpew", output_dir=custom_dir)

    assert cfg.output_dir == custom_dir.resolve()
    assert custom_dir.exists()


def test_default_format_prefers_mp4_and_m4a() -> None:
    cfg = DownloadConfig.from_inputs("https://youtu.be/8CcP8hbZpew")
    assert cfg.format_selector == "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"


def test_validate_youtube_url_rejects_other_hosts() -> None:
    with pytest.raises(InvalidURLError):
        validate_youtube_url("https://example.com/video")


def test_validate_youtube_url_accepts_short_without_scheme() -> None:
    normalized = validate_youtube_url("youtu.be/8CcP8hbZpew")
    assert normalized.startswith("https://")
