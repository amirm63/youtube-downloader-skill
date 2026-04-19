from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from .config import DownloadConfig
from .errors import DependencyError, DownloadFailedError


@dataclass(frozen=True)
class DownloadResult:
    file_path: Path
    title: str
    video_id: str


class YoutubeDownloader:
    def __init__(self, config: DownloadConfig) -> None:
        self.config = config

    def _build_options(self) -> dict:
        return {
            "format": self.config.format_selector,
            "merge_output_format": self.config.merge_output_format,
            "outtmpl": str(self.config.output_dir / "%(title)s [%(id)s].%(ext)s"),
            "noplaylist": True,
            "retries": self.config.retries,
            "socket_timeout": self.config.socket_timeout,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [self._progress_hook],
        }

    def _progress_hook(self, data: dict) -> None:
        status = data.get("status")

        if status == "downloading":
            percent = (data.get("_percent_str") or "").strip()
            speed = (data.get("_speed_str") or "").strip()
            eta = data.get("eta")
            eta_display = f"{eta}s" if eta is not None else "?"
            print(f"Fortschritt: {percent} | {speed} | ETA {eta_display}", end="\r", flush=True)
            return

        if status == "finished":
            print("\nDownload abgeschlossen, finale Datei wird vorbereitet...", flush=True)

    def _resolve_output_path(self, info: dict, ydl: YoutubeDL) -> Path:
        requested_downloads = info.get("requested_downloads") or []
        if requested_downloads:
            first = requested_downloads[0]
            candidate = first.get("filepath")
            if candidate:
                return Path(candidate)

        filepath = info.get("filepath")
        if filepath:
            return Path(filepath)

        return Path(ydl.prepare_filename(info))

    def download(self) -> DownloadResult:
        try:
            with YoutubeDL(self._build_options()) as ydl:
                info = ydl.extract_info(self.config.url, download=True)
                if info is None:
                    raise DownloadFailedError("yt-dlp hat keine Videoinformationen zuruckgegeben.")

                file_path = self._resolve_output_path(info, ydl)
                return DownloadResult(
                    file_path=file_path,
                    title=str(info.get("title") or "Unbekannter Titel"),
                    video_id=str(info.get("id") or ""),
                )
        except DownloadError as exc:
            message = str(exc)
            if "ffmpeg" in message.lower():
                raise DependencyError(
                    "ffmpeg wurde nicht gefunden. Bitte ffmpeg installieren und den Terminal neu starten."
                ) from exc
            raise DownloadFailedError(f"Download fehlgeschlagen: {message}") from exc
