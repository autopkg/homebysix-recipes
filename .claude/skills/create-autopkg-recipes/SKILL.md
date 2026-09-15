---
name: create-autopkg-recipes
description: >-
  Create AutoPkg recipes for macOS apps from vendor URLs. Use when asked to create, generate, scaffold, or add .download.recipe, .pkg.recipe, .munki.recipe, or .install.recipe files.
user-invocable: true
---

# Create AutoPkg Recipes

Create the smallest complete recipe family supported by the request, following neighboring recipes.

## 1. Preflight

- Deduplicate the input URLs.
- Search AutoPkg for existing recipes and inspect the checkout directly. Search both `.recipe` and `.recipe.yaml`; the local search index may be stale.
- If the product already has recipes, report them and ask before adding or changing duplicates.
- Ask before proceeding with Mac App Store-only, paid-without-public-trial, TestFlight/beta-only, source-only, web-only, gated-without-public-binary, dead/404, or ad-hoc/unsigned products.

## 2. Find the artifact

Identify the stable direct download, Sparkle appcast, or GitHub/Bitbucket/SourceForge project URL. Never invent a domain when resolving relative URLs.

Use HEAD first, then GET with redirects when HEAD is unsupported. Inspect redirects, `Content-Disposition`, content type, release assets, and appcast data. Do not use aggregators as the artifact source.

For GitHub releases, prefer the repository URL with `GitHubReleasesInfoProvider` and a precise `asset_regex`; avoid feeding a direct release asset URL to Recipe Robot when it may classify it as a repository.

Verify the selected artifact is the actual app, not a helper or unrelated asset. Inspect `Info.plist` and `codesign` metadata when determining bundle ID, version, architecture, and Team ID.

## 3. Generate

Use Recipe Robot for a stable binary URL, appcast, or repository URL. Configure it before running if required. Use `--ignore-existing` only for a confirmed false-positive match. If Recipe Robot is unavailable or produces an incorrect artifact, hand-author the recipes using a nearby recipe as the template.

Honor the requested format. For plist output, use `.recipe` filenames and finish with `plutil -convert xml1`; do not leave duplicate YAML variants.

## 4. Conventions

- Use one directory per app. Use a developer directory only when grouping multiple products from that developer.
- Recipe filenames contain no spaces.
- Use `com.github.homebysix.<type>.<App>` identifiers.
- Match neighboring `MinimumVersion`, inputs, processor order, and parent identifiers.
- Download recipes must include `CodeSignatureVerifier` with HTTPS sources and a concrete requirement. Quote a numeric-leading Team ID.
- For DMGs, prefer `%pathname%/App.app`; AutoPkg’s DMG-aware processors mount the image. Avoid passing temporary paths returned by a `FileFinder` mount to later processors.
- For ZIPs, use `URLDownloader`, `EndOfCheckPhase`, `Unarchiver`, `CodeSignatureVerifier`, then `Versioner`.
- Parameterize real architecture variants with `ARCH`; default to the vendor’s current architecture and document alternatives.
- Munki metadata must include both `unattended_install` and `unattended_uninstall`, a factual one-line description, and a cleaned developer name.
- Remove generated icon scratch files.

## 5. Validate

Run:

```bash
find <new-directories> -name '*.recipe' -exec plutil -convert xml1 {} \;
find <new-directories> -name '*.recipe' -exec plutil -lint {} \;
pre-commit run check-autopkg-recipes --files <new-files>
autopkg run -vvq <App>/<App>.download.recipe <App>/<App>.pkg.recipe
```

Do not run install or Munki recipes during validation. If disk-image mounting is blocked by the execution environment, distinguish that environment failure from a recipe failure and rerun the same bounded test in an allowed environment.

## 6. Report

List created files, validation results, source/signing/architecture caveats, and skipped products requiring approval or better source data. Do not commit or push unless asked.
