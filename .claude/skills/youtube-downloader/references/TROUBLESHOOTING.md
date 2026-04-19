# Troubleshooting

## Error: ffmpeg not found

Cause:
- ffmpeg is not installed or not on PATH.

Fix:
1. Install ffmpeg.
2. Restart terminal.
3. Run ffmpeg -version to verify.

## Error: invalid_url

Cause:
- URL is not YouTube, or is malformed.

Fix:
- Use full YouTube URL, for example:
  - https://www.youtube.com/watch?v=QGm7W0KZen4
  - https://youtu.be/QGm7W0KZen4

## Error: download_failed

Cause:
- Network issue, geo restriction, or platform throttling.

Fix:
1. Retry once.
2. Confirm URL opens in browser.
3. Update yt-dlp:
   python -m pip install --upgrade yt-dlp

## No sound in some players

Cause:
- Some players cannot decode certain audio or video streams.

Fix:
1. Use VLC for playback.
2. Keep default format selector from this skill (mp4+m4a preference).
3. If needed, force compatible format with --format argument in script calls.
