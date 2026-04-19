from __future__ import annotations

import argparse
import sys
from dataclasses import replace

from . import __version__
from .config import DownloadConfig
from .downloader import YoutubeDownloader
from .errors import ConfigurationError, DependencyError, DownloadFailedError, InvalidURLError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="youtube-downloader-skill",
        description="Lade ein offentliches YouTube-Video uber URL herunter.",
    )
    parser.add_argument("url", help="YouTube-URL")
    parser.add_argument(
        "--output",
        dest="output",
        default=None,
        help="Optionales Zielverzeichnis (Standard: ./Outputs)",
    )
    parser.add_argument(
        "--format",
        dest="format_selector",
        default="bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        help="yt-dlp Formatselektor (Standard: bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = DownloadConfig.from_inputs(args.url, args.output)
        config = replace(config, format_selector=args.format_selector)

        print(f"Starte Download: {config.url}")
        print(f"Zielordner: {config.output_dir}")

        result = YoutubeDownloader(config).download()
        print(f"Erfolg: {result.title}")
        print(f"Datei: {result.file_path}")
        return 0
    except InvalidURLError as exc:
        print(f"Ungultige Eingabe: {exc}", file=sys.stderr)
        return 2
    except DependencyError as exc:
        print(f"Fehlende Abhangigkeit: {exc}", file=sys.stderr)
        return 3
    except ConfigurationError as exc:
        print(f"Konfigurationsfehler: {exc}", file=sys.stderr)
        return 4
    except DownloadFailedError as exc:
        print(str(exc), file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
