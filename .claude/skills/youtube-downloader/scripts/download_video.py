#!/usr/bin/env python3
"""Standalone downloader script bundled with the Claude skill."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

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
        raise ValueError("URL must start with http or https.")

    host = parsed.netloc.lower().split(":", 1)[0]
    if host not in SUPPORTED_HOSTS and not host.endswith(".youtube.com"):
        raise ValueError("Only YouTube URLs are supported.")

    if not parsed.path or parsed.path == "/":
        raise ValueError("The provided URL looks incomplete.")

    return normalized


def resolve_output_dir(raw_output: str | None) -> Path:
    if raw_output:
        output_dir = Path(raw_output).expanduser()
        if not output_dir.is_absolute():
            output_dir = (Path.cwd() / output_dir).resolve()
        else:
            output_dir = output_dir.resolve()
    else:
        output_dir = (Path.cwd() / "Outputs").resolve()

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def build_options(output_dir: Path, format_selector: str) -> dict:
    return {
        "format": format_selector,
        "merge_output_format": "mp4",
        "outtmpl": str(output_dir / "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "retries": 3,
        "socket_timeout": 30,
        "quiet": True,
        "no_warnings": True,
    }


def resolve_downloaded_file(info: dict, ydl: YoutubeDL) -> Path:
    requested_downloads = info.get("requested_downloads") or []
    if requested_downloads:
        first = requested_downloads[0]
        file_path = first.get("filepath")
        if file_path:
            return Path(file_path)

    direct = info.get("filepath")
    if direct:
        return Path(direct)

    return Path(ydl.prepare_filename(info))


def run_download(url: str, output_dir: Path, format_selector: str) -> tuple[str, Path]:
    with YoutubeDL(build_options(output_dir, format_selector)) as ydl:
        info = ydl.extract_info(url, download=True)
        if info is None:
            raise RuntimeError("yt-dlp did not return video metadata.")

        title = str(info.get("title") or "Unknown Title")
        file_path = resolve_downloaded_file(info, ydl)
        return title, file_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a public YouTube video.")
    parser.add_argument("--url", required=True, help="YouTube URL")
    parser.add_argument("--output", default=None, help="Optional output directory")
    parser.add_argument(
        "--format",
        default="bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        help="yt-dlp format selector",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        url = validate_youtube_url(args.url)
    except ValueError as exc:
        print(f"ERROR: invalid_url: {exc}", file=sys.stderr)
        return 2

    output_dir = resolve_output_dir(args.output)

    try:
        title, file_path = run_download(url, output_dir, args.format)
    except DownloadError as exc:
        message = str(exc)
        if "ffmpeg" in message.lower():
            print("ERROR: dependency: ffmpeg not found. Install ffmpeg and retry.", file=sys.stderr)
            return 3
        print(f"ERROR: download_failed: {message}", file=sys.stderr)
        return 5
    except Exception as exc:  # defensive fallback for runtime issues
        print(f"ERROR: unexpected: {exc}", file=sys.stderr)
        return 10

    print(f"SUCCESS_TITLE={title}")
    print(f"SUCCESS_FILE={file_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
