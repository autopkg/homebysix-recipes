---
name: create-autopkg-recipes
description: |
  Create AutoPkg recipes (download, pkg, munki, install, etc.) for a macOS app
  from a vendor URL. Use whenever the user asks to create, generate, scaffold,
  or add AutoPkg recipes for an app.
  Keywords:
  - AutoPkg, autopkg
  - .download.recipe, .pkg.recipe, .munki.recipe, .install.recipe
  - Recipe Robot, recipe-robot
  - homebysix-recipes, Munki, pkg
user-invocable: true
---

# Create AutoPkg Recipes

Scaffold recipes for a macOS app following repo conventions. E2E test download+pkg before handing off.

## 1. Check for duplicates

`autopkg search <AppName>.download` (try vendor-prefixed variants too, e.g. `Google<AppName>`). Any match, any repo → surface and ask before building.

## 2. Gather metadata

Note: download URL / appcast / GH releases, developer, description, display name. Don't fully download — HEAD only (`curl -sIL`); let Recipe Robot fetch. Never fabricate a domain from a relative URL — resolve against the domain actually fetched.

If it's a normal GitHub-releases / direct-URL / Sparkle app, skip straight to step 3 — don't pre-inspect.

**Skip signals (ask first, don't silently build or drop):** Mac App Store-only; paid-only with no public trial DMG; TestFlight/beta-only; source-only (no prebuilt binary).

## 3. Recipe Robot

`/Applications/Recipe Robot.app/Contents/Resources/scripts/recipe-robot <input>`

Accepts: direct download URL, Sparkle appcast, GitHub/BitBucket/SourceForge project URL, Dropbox link, local `.app`/`.pkg`/`.dmg`/archive. Rejects marketing pages and existing `.recipe` files — find the real download/appcast/repo URL instead.

- Config error → ask user to run `--configure`.
- False "recipe exists" match → `--ignore-existing` (don't use reflexively).
- Version-pinned URL (e.g. `/v1.2.3/App.dmg`) → prepend `URLTextSearcher` against a stable page to capture the current URL.
- Modernizing an old recipe → run RR with `--ignore-existing`, diff+merge into the existing recipes rather than replacing.

No RR installed → hand-author, modeling after a repo recipe with the same delivery format.

**Gated/API-driven downloads** (HEAD returns HTML/4xx, JS-triggered download): hand-author chained `URLTextSearcher` steps to extract the real URL, feed into `URLDownloader` via `result_output_var_name: url`. Examples: `Ecosia/EcosiaBrowser.download.recipe`, `Google/Antigravity.download.recipe`.

**Structured APIs** (tracks/locales/channels, avoids duplicated regex across recipes): custom processor `<Vendor><Purpose>InfoProvider.py` subclassing `autopkglib.URLGetter`. Example: `Cocktail/CocktailReleasesInfoProvider.py`. For one URL behind an API, `URLTextSearcher` is enough.

## 4. Conventions

- Directory = app name (or developer, if one already exists for them).
- Filenames: no spaces, even if `Input/NAME` has one (e.g. `TightStudio.pkg.recipe` for app "Tight Studio").
- Identifier: `com.github.homebysix.<type>.<App>`, no spaces.
- Match `MinimumVersion`, `Input/NAME`, `ParentRecipe`, processor order to neighbors.
- Download recipe always has `CodeSignatureVerifier`. Quote `subject.OU` if it starts with a digit (`= "7D2YX5DQ6M"`) — unquoted fails at runtime despite linting fine.
- ZIP with no appcast: `URLDownloader` → `EndOfCheckPhase` → `Unarchiver` → `CodeSignatureVerifier` → `Versioner`.
- Munki `pkginfo`: set both `unattended_install` and `unattended_uninstall` to `true`. Write a factual, non-salesy one-line `description` (no marketing copy, no emojis, no blank placeholder) — verify against the app itself (mount DMG, check Info.plist, `strings` the binary) if unsure.
- Delete the app icon `.png` RR drops next to the recipes — a local scratch file, not committed.
- `plutil -lint` every file.

**Multi-arch apps:** RR won't add an `ARCH` var. Parameterize manually (`%ARCH%` in `asset_regex`/`re_pattern`/`url`), default `Input/ARCH` to `arm64`, document alternatives in `Description`. Don't set munki `supported_architectures` from `%ARCH%` (vendor/munki naming mismatches, blocks Rosetta unnecessarily) unless the binary genuinely can't run under Rosetta.

**Recognize, don't add unless asked:** `StopProcessingIf` after `EndOfCheckPhase` (marginal gain, download step already skips); pseudo-universal pkgs merging arch builds (prefer true universal build or two recipes); third-party aggregators (Homebrew/MacUpdate) as the binary/version source — go direct to vendor, each hop is a supply-chain trust cost.

## 5. Security — ask before proceeding

No code signature requirement, or insecure HTTP anywhere (download/appcast). Explain the risk; proceed only on explicit yes.

## 6. E2E test

```
autopkg run -vvq <App>/<App>.download.recipe <App>/<App>.pkg.recipe
```

Don't run install/munki — they write to `/Applications`, the munki repo, etc. Trust-info warnings on uncommitted recipes are expected.

## 7. Report

What was created, what tested clean, caveats (missing Team ID, unusual signing, dev-name mismatch, skipped tests). Don't commit or push unless asked.
