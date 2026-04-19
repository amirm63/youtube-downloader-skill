---
name: youtube-downloader
description: Downloads a public YouTube video from a URL into a local output folder. Use when the user asks to download, save, or export a YouTube video file.
argument-hint: [youtube-url] [optional-output-folder]
disable-model-invocation: true
allowed-tools: Bash(python *) Bash(py *) Bash(ffmpeg *) Read
---

# YouTube Downloader Skill

This skill downloads one public YouTube video per invocation.

## Invocation

- /youtube-downloader <youtube-url>
- /youtube-downloader <youtube-url> <output-folder>

## Workflow

1. Validate that the first argument is a YouTube URL.
2. If a second argument is provided, use it as output folder.
3. If no second argument is provided, use Outputs in the current working directory.
4. Run the helper script in this skill directory:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/download_video.py --url "$0"
```

If output folder argument is provided, run:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/download_video.py --url "$0" --output "$1"
```

5. Return a short result summary with:
- title
- final file path
- success or error

## Guardrails

- v1 supports public YouTube videos only.
- Do not use cookies or account login unless explicitly requested.
- Keep file operations local unless user asks otherwise.

## Additional References

- Setup and install: [references/INSTALL.md](references/INSTALL.md)
- Usage examples: [references/EXAMPLES.md](references/EXAMPLES.md)
- Error fixes: [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
- Validation checklist: [references/CHECKLIST.md](references/CHECKLIST.md)
