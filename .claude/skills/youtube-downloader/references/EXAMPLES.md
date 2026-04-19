# Usage Examples

## Basic download

```text
/youtube-downloader https://www.youtube.com/watch?v=QGm7W0KZen4
```

Expected behavior:
- Creates Outputs folder if missing.
- Downloads one video.
- Returns title and final file path.

## Custom output folder

```text
/youtube-downloader https://www.youtube.com/watch?v=XYmM78MGh60 ./Outputs/custom
```

Expected behavior:
- Uses ./Outputs/custom as destination.

## Invalid URL example

```text
/youtube-downloader https://example.com/video
```

Expected behavior:
- Returns invalid_url error and no download.
