from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

import pytest

from youtube_downloader_skill.config import DownloadConfig
from youtube_downloader_skill.downloader import YoutubeDownloader

EXAMPLE_URL = "https://youtu.be/8CcP8hbZpew?si=Y_3IW7Olq2PXav9Q"


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION_DOWNLOAD") != "1",
    reason="Set RUN_INTEGRATION_DOWNLOAD=1 to run network download test.",
)
def test_integration_download_example_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    config = DownloadConfig.from_inputs(EXAMPLE_URL)
    config = replace(config, format_selector="best[height<=480]/best")

    result = YoutubeDownloader(config).download()

    assert result.file_path.exists()
    assert (tmp_path / "Outputs") in result.file_path.parents
