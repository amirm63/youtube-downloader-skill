"""Custom error types for predictable CLI handling."""


class DownloaderError(Exception):
    """Base class for all downloader errors."""


class ConfigurationError(DownloaderError):
    """Raised for invalid runtime configuration."""


class InvalidURLError(ConfigurationError):
    """Raised when URL input is invalid or unsupported."""


class DependencyError(DownloaderError):
    """Raised when required system dependencies are missing."""


class DownloadFailedError(DownloaderError):
    """Raised when yt-dlp cannot complete a download."""
