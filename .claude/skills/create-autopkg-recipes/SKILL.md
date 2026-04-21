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

Scaffold recipes for a macOS app following the current repo's conventions. E2E test the download and pkg before handing off.

## 1. Check for existing recipes

Run `autopkg search <AppName>.download` (chains start at `.download`; filters noise). Try vendor-prefixed variants too (e.g. `Google<AppName>.download`). If anything matches — in any repo — surface it and ask before building. Don't duplicate.

## 2. Gather metadata — no full download

From the vendor page, note: download URL (or appcast / GH releases), developer, description, display name.

**Validate URLs with HEAD only** (`curl -sIL <url>`), never a full download. Apps can be huge; Recipe Robot will do its own fetch. Only download to `/tmp/` and inspect by hand (`plutil -p`, `codesign -dvvv`, `codesign -d -r-`) if Recipe Robot fails. Never inspect inside the repo.

**Non-fit signals — surface early and ask before building:**
- **Mac App Store-only** (vendor page's only download link is `apps.apple.com/app/...`, or page says "available on the Mac App Store"). AutoPkg's normal pipeline can't fetch MAS apps — they require an authenticated Apple ID via `mas` CLI or `nmcspadden-recipes`' `AppStoreApp` processor, and redistribution through munki/pkg is licensing-constrained. Default: skip.
- **Paid-only with no trial build** (download gated behind purchase/login, no public DMG). `CodeSignatureVerifier` can't be wired up without an artifact to inspect. Default: skip unless the user has a licensed download URL to provide.
- **TestFlight / beta-only**. Not redistributable.
- **Source-only / build-from-source** (vendor instructs `git clone` + `make`; no pre-built DMG/ZIP/PKG, no GitHub releases). No vendor binary to fetch or signature to verify. Default: skip.

Surface the signal and ask; don't silently proceed.

## 3. Prefer Recipe Robot

`/Applications/Recipe Robot.app/Contents/Resources/scripts/recipe-robot <input>`

**Accepts:** direct download URL; Sparkle appcast (`.xml`/`.rss`/`.php` or `appcast` in URL); GitHub / BitBucket / SourceForge project URL; Dropbox shared link; local `.app` (reads `SUFeedURL` from Info.plist), `.pkg`, `.dmg`, or archive (`.zip` etc.). For local files without a known source, RR falls back to the `kMDItemWhereFroms` xattr to find the download URL. **Rejects** marketing pages and existing `.recipe` files — for a marketing page, find the actual download/appcast/repo URL behind it.

- Config error → ask user to run `--configure` and wait.
- "Recipes exist" and detection is wrong → re-run with `--ignore-existing`. Don't use reflexively.
- **Version-pinned URL** (e.g. `/v1.2.3/App.dmg`): run RR to scaffold, then prepend a `URLTextSearcher` targeting a stable page to capture the current URL, wire its output into `URLDownloader`. Otherwise the recipe pins forever.
- **Modernizing old recipes**: copy the URL from the existing `.download`, run RR with `--ignore-existing`, then diff+merge into the existing recipes. Don't wholesale replace — preserves customizations while picking up new conventions (e.g. `AppPkgCreator`).

If RR isn't installed, hand-author by modeling after a repo recipe matching your delivery format (DMG/ZIP/PKG/appcast/GH releases/direct URL).

### 3a. Gated/API-driven downloads

Signs: HEAD returns HTML or 4xx; download button triggers an XHR; JS required. RR can't handle these — hand-author with chained `URLTextSearcher` steps extracting the real URL (and intermediate tokens), feeding `URLDownloader` via `result_output_var_name: url`. References:
- `Ecosia/EcosiaBrowser.download.recipe` — single `URLTextSearcher` against a JSON-like API.
- `Google/Antigravity.download.recipe` — two chained: HTML page → JS bundle name → DMG URL inside JS source.

Scrape JS sources as strings; don't try to execute.

### 3b. Custom processors for structured APIs

When an API returns structured data (tracks/locales/OS-keyed bundle IDs/channels) and multiple recipes would otherwise duplicate regex logic, write a custom processor instead:
- Name: `<Vendor><Purpose>InfoProvider.py` or `<Vendor>URLProvider.py`.
- Subclass `autopkglib.URLGetter`.
- Clean `input_variables` (defaults) + `output_variables` (`url`, `version`, `bundle_id`).
- Keep per-release mapping in a module-level dict.

Reference: `Cocktail/CocktailReleasesInfoProvider.py`. For a single URL behind an API, `URLTextSearcher` is fine — don't over-engineer.

## 4. Repo conventions

- Directory named after the app (or the developer, if one already exists for them).
- Identifier namespace `com.github.homebysix.<type>.<App>`.
- Consistent `MinimumVersion`, `Input/NAME`, `ParentRecipe`, processor order with neighbors.
- Download recipe **always** includes `CodeSignatureVerifier` with the app's designated requirement. **Quote any `subject.OU` value that starts with a digit** (e.g. `= "7D2YX5DQ6M"`, not `= 7D2YX5DQ6M`) — the codesign requirement parser fails at runtime on unquoted digit-leading OUs even though the recipe lints fine. Recipe Robot sometimes emits the unquoted form; fix it if your Team ID starts with a digit.
- ZIP with no appcast: `URLDownloader` → `EndOfCheckPhase` → `Unarchiver` → `CodeSignatureVerifier` → `Versioner`.
- `plutil -lint` every file.

### 4a. Multi-architecture apps

RR doesn't add an `ARCH` variable — its default regex matches multiple variants non-deterministically. Parameterize manually:
- `GitHubReleasesInfoProvider` → `%ARCH%` in `asset_regex` (e.g. `.*-%ARCH%\.dmg$`).
- `URLTextSearcher` → `%ARCH%` in `re_pattern` or `url`.
- Static `URLDownloader` → `%ARCH%` in `url`.

Set `Input/ARCH` default (usually `arm64`) and document alternatives in `Description` (see `Google/Antigravity.download.recipe`).

**Don't pipe `%ARCH%` into munki's `supported_architectures`:**
1. Vendor names (`x64`, `amd64`, `intel`) rarely match munki's (`x86_64`, `arm64`) — translating needs `FindAndReplace` and silently breaks targeting if wrong.
2. `x86_64`-only blocks Rosetta 2 installs on Apple Silicon, which is usually desirable to allow. Unset (munki's default) is normally correct.

Set it only when the binary genuinely won't run under Rosetta (arm64-only, Intel-only kext).

### 4b. Antipatterns (recognize, don't recommend)

Functional but not conventions here. Don't add proactively; do them only if asked.
- **`StopProcessingIf` after `EndOfCheckPhase`** to skip pkg/munki steps when the download is unchanged. Modest savings; AutoPkg already skips the download itself.
- **Pseudo-universal installers** merging Intel + arm64 into one arch-conditional pkg. Prefer a true universal vendor build or two parameterized recipes — munki is arch-aware natively and Jamf can gate by smart groups. Only consider the merged form if the deployment platform can't target by arch, and flag it as a workaround.
- **Third-party aggregator URLs** (Homebrew formulas/taps, MacUpdate, download aggregators) as the download or version source. Each intermediary is a **supply-chain trust hop** — a party who can be compromised, rewrite the binary, stop maintaining the formula, or redistribute under different terms. Every added step expands the set of parties the downstream sysadmin has to trust. Go direct to the vendor's source URL. Partial exception: scraping a Homebrew tap *only* to discover the current version string, then downloading from the vendor's own host when the vendor doesn't publish a version manifest — see `Cosine/cos.download.recipe`. Still sub-ideal; a vendor-hosted version endpoint would be strictly better. Apply the same "minimize trust hops" lens to any recipe that chains through intermediaries for the binary itself.

## 5. Security gates — require explicit approval

Stop and ask before proceeding if:
- **No code signature requirement** (unsigned source or `CodeSignatureVerifier` omitted) — breaks AutoPkg's integrity check.
- **Insecure HTTP** anywhere (download, appcast) — MITM-vulnerable.

Explain the risk; proceed only on a clear yes.

## 6. E2E test — download and pkg only

```
autopkg run -vvq <App>/<App>.download.recipe <App>/<App>.pkg.recipe
```

Verify fetch → unarchive → signature → version, and that pkg lands at the expected path. **Don't run** `install`/`munki`/etc — they write to `/Applications`, the munki repo, etc. Trust-info warnings on uncommitted recipes are expected.

## 7. Report

Summarize what was created, what ran clean, and any caveats (missing Team ID, unusual signing, dev-name mismatch, skipped tests). Don't commit or push unless asked.
