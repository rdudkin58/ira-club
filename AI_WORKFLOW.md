# AI workflow

## Primary maintainer
This repository is now maintained with ChatGPT as the primary AI engineering assistant.

## Before every change
- Read `PROJECT_CONTEXT.md`.
- Inspect current `main` and relevant files.
- Check open PRs and recent related commits.
- Check whether `ira-psiholog` is affected.
- Do not use old `claude/*` branches as a source of truth unless explicitly comparing historical work.

## Git workflow
- Normal implementation: feature branch → review → PR → merge.
- Never force-push or rewrite history unless explicitly requested.
- Do not delete historical Claude branches without a separate cleanup decision.
- Avoid direct commits to `main` for functional changes.

## Verification
For site changes:
- inspect changed HTML/CSS/JS;
- verify links/references and obvious JavaScript syntax;
- verify no secrets or client data were introduced;
- verify sensitive pages remain excluded from analytics where required.

For cross-repository changes:
- inspect both repositories before implementation;
- test the complete flow where possible.

## Production
Repository state and live production state are different facts. Never claim DNS, TLS, Cloudflare deployment, Telegram webhook, Telegram Business connection, or Robokassa configuration is live unless independently verified.

## Sensitive data
Never commit:
- Telegram exports;
- client databases;
- passwords;
- API tokens;
- Cloudflare secrets;
- Robokassa credentials;
- other personal/client data.

## Communication
When reporting work, distinguish:
1. changed;
2. verified;
3. not verified / requires dashboard or production access;
4. recommended next action.
