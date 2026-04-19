from __future__ import annotations

from pathlib import Path

import pytest

from youtube_downloader_skill.cli import main
from youtube_downloader_skill.downloader import DownloadResult
from youtube_downloader_skill.errors import DependencyError


class DummyDownloader:
    def __init__(self, config) -> None:
        self.config = config

    def download(self) -> DownloadResult:
        output_file = self.config.output_dir / "demo.mp4"
        output_file.write_text("ok", encoding="utf-8")
        return DownloadResult(file_path=output_file, title="Demo", video_id="abc123")


class DependencyFailingDownloader:
    def __init__(self, config) -> None:
        self.config = config

    def download(self) -> DownloadResult:
        raise DependencyError("ffmpeg fehlt")


def test_cli_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("youtube_downloader_skill.cli.YoutubeDownloader", DummyDownloader)

    exit_code = main(["https://youtu.be/8CcP8hbZpew"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Erfolg:" in captured.out
    assert (tmp_path / "Outputs").exists()


def test_cli_invalid_url(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["https://example.com/video"])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Ungultige Eingabe" in captured.err


def test_cli_dependency_error(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("youtube_downloader_skill.cli.YoutubeDownloader", DependencyFailingDownloader)

    exit_code = main(["https://youtu.be/8CcP8hbZpew"])
    captured = capsys.readouterr()

    assert exit_code == 3
    assert "Fehlende Abhangigkeit" in captured.err
