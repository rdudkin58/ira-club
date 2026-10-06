# Project Context — ira-club

> Canonical working context for the project. This file replaces assistant-specific memory as the primary project handoff document. It contains no secrets and no client personal data.

## Repositories
- Frontend/site: https://github.com/rdudkin58/ira-club
- Backend/automation: https://github.com/rdudkin58/ira-psiholog
- Production domain: https://irina-psiholog.ru
- Default branch: `main`
- Hosting: GitHub Pages
- Site type: static HTML/CSS/JS

## Operating rule
Treat `main` as the current source of truth for production-intended code. Before changing anything:
1. inspect current `main`;
2. inspect related open PRs;
3. check whether the requested change affects the other repository;
4. identify production dependencies (GitHub Pages, Cloudflare Workers, Telegram, Robokassa, DNS);
5. make the smallest safe change;
6. verify the result;
7. report exactly what changed and what remains unverified.

Do not infer live production state from repository contents alone.

## Project
The site is the public frontend for Irina Dudkina's psychology practice and the closed women's club «МОЁ СОСТОЯНИЕ». It contains:
- landing pages;
- lead-magnet tests;
- diagnostic CTAs;
- marathon/product pages;
- legal pages;
- internal recommendation/operations pages;
- a browser-local Telegram export analyzer.

## Content rules
- Russian language.
- Address women on «ты».
- The club name is always: закрытый клуб «МОЁ СОСТОЯНИЕ».
- Irina's voice: warm, lively, practical, energetic, with a gentle «пендаль», without academic jargon.
- Do not promise «три конкретных шага» after the free diagnostic.
- Diagnostic duration: 40 minutes, free.
- Main product: «Равновесие».
- Never invent current prices or product terms; verify against current project context before editing commercial copy.

## Privacy / security
- Never commit client personal data, Telegram exports, client spreadsheets, passwords, tokens, API keys, or Cloudflare/Robokassa secrets.
- `noindex` is not access control.
- Client-message analysis must remain local unless an explicit secure backend is designed and approved.
- Do not add analytics to pages containing client data.
- Treat internal pages as potentially sensitive even if they are not linked from the public site.

## Current known production-sensitive items
- `CNAME` points to `irina-psiholog.ru`.
- GitHub Pages deployment is branch-based; there is no confirmed Actions deployment pipeline.
- Draft PR #86 contains legal/privacy changes and is not merged. Do not assume those changes are in production.
- `razbor-perepisok-3b5e9d5f.html` handles Telegram exports locally in the browser and requires stronger access-control consideration before broad production use.
- Yandex Metrika is intentionally excluded from the client-message analysis/password-sensitive pages.

## Change policy
Functional changes should normally be made through a dedicated branch and PR. Do not delete old Claude branches merely because they are named `claude/*`; classify them first and preserve history until no longer needed.
