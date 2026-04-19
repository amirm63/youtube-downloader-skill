from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .errors import InvalidURLError


SUPPORTED_HOSTS = {
    "youtu.be",
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
}


def normalize_url(url: str) -> str:
    cleaned = url.strip()
    if not cleaned:
        return cleaned

    parsed = urlparse(cleaned)
    if parsed.scheme:
        return cleaned

    if cleaned.startswith(("youtu.be/", "youtube.com/", "www.youtube.com/")):
        return f"https://{cleaned}"

    return cleaned


def validate_youtube_url(url: str) -> str:
    normalized = normalize_url(url)
    parsed = urlparse(normalized)

    if parsed.scheme not in {"http", "https"}:
        raise InvalidURLError("Die URL muss mit http oder https beginnen.")

    host = parsed.netloc.lower().split(":", 1)[0]
    if host not in SUPPORTED_HOSTS and not host.endswith(".youtube.com"):
        raise InvalidURLError("Nur YouTube-URLs werden unterstutzt.")

    if not parsed.path or parsed.path == "/":
        raise InvalidURLError("Die YouTube-URL scheint unvollstandig zu sein.")

    return normalized


def default_output_dir(cwd: Path | None = None) -> Path:
    base_dir = (cwd or Path.cwd()).resolve()
    return base_dir / "Outputs"


@dataclass(frozen=True)
class DownloadConfig:
    url: str
    output_dir: Path
    format_selector: str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    merge_output_format: str = "mp4"
    retries: int = 3
    socket_timeout: int = 30

    @classmethod
    def from_inputs(cls, url: str, output_dir: str | Path | None = None) -> "DownloadConfig":
        normalized_url = validate_youtube_url(url)

        if output_dir is None:
            resolved_output_dir = default_output_dir()
        else:
            raw_path = Path(output_dir).expanduser()
            resolved_output_dir = raw_path.resolve() if raw_path.is_absolute() else (Path.cwd() / raw_path).resolve()

        resolved_output_dir.mkdir(parents=True, exist_ok=True)
        return cls(url=normalized_url, output_dir=resolved_output_dir)
