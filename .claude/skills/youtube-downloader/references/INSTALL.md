# Installation Guide

This guide covers Claude Code and Claude.ai installation paths.

## 1) Claude Code project skill

Use this repo as-is. Claude Code auto-discovers project skills in .claude/skills.

1. Clone repository.
2. Open the repository folder in Claude Code.
3. Verify the skill appears with /youtube-downloader.

## 2) Claude Code personal skill

Install for all projects by copying the skill folder.

1. Create destination folder:
   - ~/.claude/skills/youtube-downloader/
2. Copy these files into it:
   - SKILL.md
   - scripts/download_video.py
   - references/

## 3) Claude.ai upload

1. Zip only the skill folder contents where SKILL.md is at the zip root.
2. In Claude.ai open Settings > Capabilities > Skills.
3. Upload the zip.

## Dependencies

Required:
- Python 3.10+
- yt-dlp
- ffmpeg in PATH

Install example:

```bash
python -m pip install --upgrade yt-dlp
```

Windows ffmpeg example with winget:

```powershell
winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements
```
