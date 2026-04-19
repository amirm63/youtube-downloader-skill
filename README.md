# YouTube Downloader Skill for Claude

Claude skill for downloading YouTube videos from URL.

## Claude Skill

Use this skill when you want Claude to download a public YouTube video from URL.

### Install As Claude Skill

#### Option A: Project skill (recommended)

1. Clone this repository.
2. Open it in Claude Code.
3. Invoke with /youtube-downloader <url>.

Claude Code discovers .claude/skills automatically for project scope.

#### Option B: Personal skill

Copy .claude/skills/youtube-downloader to:

- ~/.claude/skills/youtube-downloader

Then restart Claude Code if the top-level skills directory did not exist before session start.

#### Option C: Claude.ai upload

1. Zip the skill folder so SKILL.md is included.
2. Upload via Claude.ai > Settings > Capabilities > Skills.

### Build Shareable Skill Zip

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package-skill.ps1
```

Output:

- dist/youtube-downloader-skill.zip

## What This Repository Contains

1. A Claude skill packaged under .claude/skills/youtube-downloader.
2. A Python CLI downloader for local execution.

## Features

- One URL input workflow
- Auto-creates Outputs folder when missing
- Public YouTube videos only in v1
- Audio compatibility fix for Windows players (prefers mp4 + m4a)
- Claude skill packaging for project, personal, and Claude.ai upload flows

## Repository Layout

- .claude/skills/youtube-downloader/SKILL.md: skill entrypoint (required)
- .claude/skills/youtube-downloader/scripts/download_video.py: standalone script used by the skill
- .claude/skills/youtube-downloader/references/: install, examples, troubleshooting, checklist
- src/youtube_downloader_skill/: Python CLI package
- scripts/install-deps-windows.ps1: dependency helper for local development

## Local CLI (Optional)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Optional dependency helper:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-deps-windows.ps1
```

Run downloader:

```powershell
python -m youtube_downloader_skill "<youtube-url>"
```

Custom output folder:

```powershell
python -m youtube_downloader_skill "<youtube-url>" --output ".\Outputs\custom"
```
